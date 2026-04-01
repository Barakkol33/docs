import argparse
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

DEFAULT_CSS = r"""
/* Professional document theme for markdown-pdf (PyMuPDF Story). */

body {
  font-family: "Georgia", "Times New Roman", "Noto Serif", serif;
  font-size: 11pt;
  line-height: 1.65;
  color: #1a1a1a;
}

h1, h2, h3, h4, h5, h6 {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Noto Sans", sans-serif;
  color: #1a1a2e;
  line-height: 1.25;
  margin-top: 22pt;
  margin-bottom: 8pt;
}
h1 {
  font-size: 26pt;
  font-weight: 700;
  border-bottom: 2.5px solid #1a1a2e;
  padding-bottom: 8pt;
  margin-bottom: 12pt;
}
h2 {
  font-size: 18pt;
  font-weight: 600;
  color: #2d2d4e;
  border-bottom: 1px solid #d1d5db;
  padding-bottom: 5pt;
  margin-top: 26pt;
}
h3 {
  font-size: 13pt;
  font-weight: 600;
  color: #374151;
}

p {
  margin: 7pt 0;
  text-align: justify;
}

ul, ol {
  margin: 6pt 0 12pt 18pt;
}
li {
  margin: 4pt 0;
}

strong {
  color: #111827;
}

a {
  color: #1d4ed8;
  text-decoration: none;
}

blockquote {
  margin: 12pt 0;
  padding: 10pt 14pt;
  border-left: 3.5px solid #6366f1;
  background: #f5f3ff;
  color: #374151;
  font-style: italic;
}

hr {
  border: none;
  border-top: 1px solid #d1d5db;
  margin: 18pt 0;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 9.5pt;
  background: #f3f4f6;
  color: #1e293b;
  padding: 1.5pt 4pt;
  border-radius: 3pt;
  border: 0.5px solid #e5e7eb;
}

pre {
  background: #f8f9fa;
  color: #1e293b;
  padding: 12pt 14pt;
  border-radius: 6pt;
  overflow: hidden;
  border: 1px solid #d1d5db;
  margin: 10pt 0;
}
pre code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  border: none;
  color: inherit;
  font-size: 9pt;
  line-height: 1.5;
}

table {
  border-collapse: collapse;
  margin: 12pt 0;
  width: 100%;
  font-size: 10.5pt;
}
th, td {
  border: 1px solid #d1d5db;
  padding: 7pt 10pt;
  vertical-align: top;
}
th {
  background: #f1f5f9;
  color: #1e293b;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Noto Sans", sans-serif;
  font-weight: 600;
  font-size: 10pt;
  text-transform: uppercase;
  letter-spacing: 0.3pt;
}
tr:nth-child(even) td {
  background: #fafafa;
}
"""


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown to a styled PDF.")
    parser.add_argument("input", type=Path, help="Path to a .md file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output PDF path (default: ./<stem>.pdf)",
    )
    parser.add_argument("--title", default=None, help="PDF title metadata (default: input stem)")
    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable PDF bookmarks (table-of-contents metadata)",
    )
    parser.add_argument(
        "--paper",
        default="A4",
        help="Paper size for PyMuPDF (default: A4)",
    )
    parser.add_argument(
        "--css",
        type=Path,
        default=None,
        help="Path to a CSS file to apply (default: built-in theme)",
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Optimize output PDF (can reduce size, may take longer)",
    )
    args = parser.parse_args()

    input_file: Path = args.input
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")

    output_file = args.output if args.output is not None else Path(f"{input_file.stem}.pdf")

    css = DEFAULT_CSS if args.css is None else _read_text(args.css)
    content = _read_text(input_file)

    pdf = MarkdownPdf(optimize=args.optimize)
    pdf.meta["title"] = args.title or input_file.stem
    pdf.add_section(
        Section(
            content,
            toc=not args.no_toc,
            root=str(input_file.parent),
            paper_size=args.paper,
            borders=(48, 54, -48, -54),
        ),
        user_css=css,
    )
    pdf.save(output_file)


if __name__ == "__main__":
    main()
