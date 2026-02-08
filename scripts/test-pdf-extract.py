#!/usr/bin/env python3
"""Test different pymupdf4llm extraction strategies on a single PDF."""

import sys
import time
from pathlib import Path

import pymupdf4llm
import pymupdf

def test_write_images(pdf_path: Path, out_dir: Path):
    """Strategy 1: write_images=True — auto-detects vector drawings, renders as PNG."""
    label = "write_images"
    d = out_dir / label
    d.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    md = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(d),
        image_format="png",
        dpi=200,
    )
    elapsed = time.perf_counter() - t0

    md_file = d / "output.md"
    md_file.write_text(md, encoding="utf-8")

    images = list(d.glob("*.png"))
    print(f"[{label}] {elapsed:.1f}s | {len(md)} chars | {len(images)} images → {d}")
    return md


def test_page_chunks(pdf_path: Path, out_dir: Path):
    """Strategy 2: page_chunks=True — structured per-page output."""
    label = "page_chunks"
    d = out_dir / label
    d.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    chunks = pymupdf4llm.to_markdown(
        str(pdf_path),
        page_chunks=True,
        write_images=True,
        image_path=str(d),
        image_format="png",
        dpi=200,
    )
    elapsed = time.perf_counter() - t0

    # chunks is a list of dicts with 'metadata' and 'text'
    full_md = ""
    for i, chunk in enumerate(chunks):
        page_num = chunk.get("metadata", {}).get("page", i + 1)
        full_md += f"\n---\n## Page {page_num}\n\n{chunk['text']}\n"

    md_file = d / "output.md"
    md_file.write_text(full_md, encoding="utf-8")

    images = list(d.glob("*.png"))
    print(f"[{label}] {elapsed:.1f}s | {len(full_md)} chars | {len(images)} images → {d}")
    return full_md


def test_hybrid(pdf_path: Path, out_dir: Path):
    """Strategy 3: Hybrid — pymupdf4llm for text + manual full-page render for visual pages."""
    label = "hybrid"
    d = out_dir / label
    d.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()

    # First: get markdown with images
    md = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(d),
        image_format="png",
        dpi=200,
    )

    # Second: detect "visual" pages (pages where text is sparse relative to graphics)
    doc = pymupdf.open(str(pdf_path))
    visual_pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        drawings = page.get_drawings()
        images_on_page = page.get_images()

        text_len = len(text)
        drawing_count = len(drawings)
        image_count = len(images_on_page)

        # Heuristic: if drawings dominate over text, it's a visual page
        is_visual = (drawing_count > 20 and text_len < 500) or (drawing_count > 50)
        if is_visual:
            visual_pages.append(i)
            # Render full page as PNG
            scale = 200 / 72.0
            mat = pymupdf.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_path = d / f"fullpage-{i+1:02d}.png"
            pix.save(str(img_path))

    doc.close()
    elapsed = time.perf_counter() - t0

    # Append visual page references to markdown
    if visual_pages:
        md += "\n\n---\n## Full-page renders (visual pages)\n\n"
        for p in visual_pages:
            md += f"![Page {p+1}](fullpage-{p+1:02d}.png)\n\n"

    md_file = d / "output.md"
    md_file.write_text(md, encoding="utf-8")

    all_images = list(d.glob("*.png"))
    print(f"[{label}] {elapsed:.1f}s | {len(md)} chars | {len(all_images)} imgs ({len(visual_pages)} full-page) → {d}")
    print(f"  Visual pages: {[p+1 for p in visual_pages]}")
    return md


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test-pdf-extract.py <input.pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.exists():
        print(f"Not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = pdf_path.parent / f"_test-extract-{pdf_path.stem}"
    out_dir.mkdir(exist_ok=True)
    print(f"PDF: {pdf_path.name}")
    print(f"Out: {out_dir}\n")

    test_write_images(pdf_path, out_dir)
    test_page_chunks(pdf_path, out_dir)
    test_hybrid(pdf_path, out_dir)

    print("\nDone. Compare outputs in:", out_dir)


if __name__ == "__main__":
    main()
