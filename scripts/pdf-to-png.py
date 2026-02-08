#!/usr/bin/env python3
"""Convert PDF pages to PNG images with max dimension ≤ 2000px.

Usage:
    python scripts/pdf-to-png.py <input.pdf> [--max-px 2000] [--dpi 150] [--pages 1-10]

Output goes to a sibling directory named after the PDF, e.g.:
    sources/fact--q3-2025.pdf → sources/fact--q3-2025/page-01.png
"""

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse page spec like '1-10' or '5' into 0-based page indices."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            start = max(int(a) - 1, 0)
            end = min(int(b), total)
            pages.extend(range(start, end))
        else:
            idx = int(part) - 1
            if 0 <= idx < total:
                pages.append(idx)
    return sorted(set(pages))


def render_page(page: fitz.Page, dpi: int, max_px: int) -> fitz.Pixmap:
    """Render a page at given DPI, then downscale if any dimension > max_px."""
    scale = dpi / 72.0
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    if pix.width <= max_px and pix.height <= max_px:
        return pix

    # Downscale to fit within max_px
    ratio = min(max_px / pix.width, max_px / pix.height)
    new_scale = scale * ratio
    mat = fitz.Matrix(new_scale, new_scale)
    return page.get_pixmap(matrix=mat, alpha=False)


def main():
    parser = argparse.ArgumentParser(description="PDF → PNG with max dimension cap")
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("--max-px", type=int, default=2000, help="Max pixel dimension (default: 2000)")
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI before capping (default: 150)")
    parser.add_argument("--pages", type=str, default=None, help="Page range, e.g. '1-10' (default: all)")
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = pdf_path.parent / pdf_path.stem
    out_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    total = len(doc)

    if args.pages:
        page_indices = parse_pages(args.pages, total)
    else:
        page_indices = list(range(total))

    print(f"Converting {len(page_indices)} pages from {pdf_path.name} (max {args.max_px}px, {args.dpi} DPI)")

    for i in page_indices:
        page = doc[i]
        pix = render_page(page, args.dpi, args.max_px)
        out_file = out_dir / f"page-{i + 1:02d}.png"
        pix.save(str(out_file))
        print(f"  {out_file.name}  {pix.width}x{pix.height}")

    doc.close()
    print(f"Done → {out_dir}")


if __name__ == "__main__":
    main()
