#!/usr/bin/env python3
"""Smart PDF → Markdown converter with visual page detection.

Text-heavy pages get extracted as markdown.
Visual pages (charts, diagrams) get rendered as full-page PNGs.

Usage:
    python scripts/pdf-to-md.py <input.pdf> [--dpi 150] [--max-px 2000] [--pages 1-10]
    python scripts/pdf-to-md.py <input.pdf> --force-render   # render ALL pages as PNG
    python scripts/pdf-to-md.py <input.pdf> --force-text     # extract ALL pages as text only

Output:
    sources/fact--q3-report.md          (markdown with embedded image refs)
    sources/fact--q3-report-images/     (PNG renders of visual pages)
"""

import argparse
import sys
from pathlib import Path

import pymupdf
import pymupdf4llm


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse page spec like '1-10' or '3,5,7' into 0-based indices."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(max(int(a) - 1, 0), min(int(b), total)))
        else:
            idx = int(part) - 1
            if 0 <= idx < total:
                pages.append(idx)
    return sorted(set(pages))


def classify_page(page: pymupdf.Page) -> dict:
    """Classify a page as text-heavy or visual based on content heuristics."""
    text = page.get_text().strip()
    drawings = page.get_drawings()
    images = page.get_images()

    text_len = len(text)
    drawing_count = len(drawings)
    image_count = len(images)

    # Visual indicators
    has_many_drawings = drawing_count > 5
    has_images = image_count > 2
    text_is_sparse = text_len < 500
    ratio = text_len / max(drawing_count, 1)

    # A page is visual if it has significant graphical content
    # relative to its text content
    is_visual = (
        (has_many_drawings and ratio < 60)
        or (has_many_drawings and text_is_sparse)
        or (has_images and text_is_sparse)
    )

    # A page has useful text if there's enough flowing text
    has_text = text_len > 100

    # Near-empty pages (title slides, dividers)
    is_empty = text_len < 50 and drawing_count < 3 and image_count < 2

    return {
        "text_len": text_len,
        "drawing_count": drawing_count,
        "image_count": image_count,
        "ratio": ratio,
        "is_visual": is_visual,
        "has_text": has_text,
        "is_empty": is_empty,
    }


def render_page_png(page: pymupdf.Page, dpi: int, max_px: int) -> pymupdf.Pixmap:
    """Render page to pixmap, capped at max_px."""
    scale = dpi / 72.0
    mat = pymupdf.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    if pix.width > max_px or pix.height > max_px:
        ratio = min(max_px / pix.width, max_px / pix.height)
        mat = pymupdf.Matrix(scale * ratio, scale * ratio)
        pix = page.get_pixmap(matrix=mat, alpha=False)

    return pix


def extract_text_pages(pdf_path: str, page_indices: list[int]) -> dict[int, str]:
    """Extract markdown text per page using pymupdf4llm."""
    chunks = pymupdf4llm.to_markdown(
        pdf_path,
        page_chunks=True,
        write_images=False,
    )
    result = {}
    for chunk in chunks:
        page_idx = chunk.get("metadata", {}).get("page", 0)
        if page_idx in page_indices:
            text = chunk.get("text", "").strip()
            if text:
                result[page_idx] = text
    return result


def main():
    parser = argparse.ArgumentParser(description="Smart PDF → Markdown + PNG")
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI (default: 150)")
    parser.add_argument("--max-px", type=int, default=2000, help="Max pixel dimension (default: 2000)")
    parser.add_argument("--pages", type=str, default=None, help="Page range, e.g. '1-10'")
    parser.add_argument("--force-render", action="store_true", help="Render ALL pages as PNG")
    parser.add_argument("--force-text", action="store_true", help="Extract ALL pages as text only")
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    doc = pymupdf.open(str(pdf_path))
    total = len(doc)

    if args.pages:
        page_indices = parse_pages(args.pages, total)
    else:
        page_indices = list(range(total))

    # Phase 1: Classify pages
    print(f"Analyzing {len(page_indices)} pages from {pdf_path.name}...")
    classifications = {}
    for i in page_indices:
        c = classify_page(doc[i])
        if args.force_render:
            c["is_visual"] = True
        if args.force_text:
            c["is_visual"] = False
            c["has_text"] = True
        classifications[i] = c

    visual_pages = [i for i in page_indices if classifications[i]["is_visual"]]
    text_pages = [i for i in page_indices if classifications[i]["has_text"]]
    empty_pages = [i for i in page_indices if classifications[i]["is_empty"]]

    print(f"  Visual: {len(visual_pages)} pages → will render PNG")
    print(f"  Text:   {len(text_pages)} pages → will extract markdown")
    print(f"  Empty:  {len(empty_pages)} pages → will skip")

    # Phase 2: Extract text for text-capable pages
    print("Extracting text...")
    text_data = extract_text_pages(str(pdf_path), set(page_indices))

    # Phase 3: Render visual pages
    img_dir = pdf_path.parent / f"{pdf_path.stem}-images"
    if visual_pages:
        img_dir.mkdir(exist_ok=True)

    print("Rendering visual pages...")
    rendered = {}
    for i in visual_pages:
        pix = render_page_png(doc[i], args.dpi, args.max_px)
        img_name = f"page-{i + 1:02d}.png"
        img_path = img_dir / img_name
        pix.save(str(img_path))
        rendered[i] = img_name
        size_kb = img_path.stat().st_size / 1024
        print(f"  p{i+1:02d}: {pix.width}x{pix.height} ({size_kb:.0f} KB)")

    doc.close()

    # Phase 4: Assemble markdown
    md_parts = []
    img_dir_rel = f"{pdf_path.stem}-images"

    for i in page_indices:
        c = classifications[i]
        if c["is_empty"] and i not in rendered and i not in text_data:
            continue

        md_parts.append(f"\n---\n\n## Page {i + 1}\n")

        # Visual page: image first
        if i in rendered:
            md_parts.append(f"\n![Page {i + 1}]({img_dir_rel}/{rendered[i]})\n")

        # Text content (below image if both exist)
        if i in text_data and c["has_text"]:
            text = text_data[i]
            # Clean up excessive blank lines
            import re
            text = re.sub(r"\n{4,}", "\n\n\n", text)
            md_parts.append(f"\n{text}\n")

    md_content = "".join(md_parts)

    # Write output
    out_path = pdf_path.with_suffix(".md")
    out_path.write_text(md_content, encoding="utf-8")

    total_img_size = sum(f.stat().st_size for f in img_dir.glob("*.png")) if visual_pages else 0
    print(f"\nOutput:")
    print(f"  Markdown: {out_path.name} ({len(md_content):,} chars)")
    if visual_pages:
        print(f"  Images:   {img_dir_rel}/ ({len(rendered)} files, {total_img_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
