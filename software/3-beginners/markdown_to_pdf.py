import argparse
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

DEFAULT_CSS = r"""
/* A simple, readable, colorful theme for markdown-pdf (PyMuPDF Story). */

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Noto Sans", sans-serif;
  font-size: 11pt;
  line-height: 1.55;
  color: #111827; /* gray-900 */
}

h1, h2, h3, h4, h5, h6 {
  color: #0f172a; /* slate-900 */
  line-height: 1.2;
  margin-top: 18pt;
  margin-bottom: 8pt;
}
h1 { font-size: 24pt; border-bottom: 2px solid #e5e7eb; padding-bottom: 6pt; }
h2 { font-size: 18pt; border-bottom: 1px solid #e5e7eb; padding-bottom: 4pt; }
h3 { font-size: 14pt; }

p { margin: 6pt 0; }
ul, ol { margin: 6pt 0 10pt 16pt; }
li { margin: 3pt 0; }

a {
  color: #2563eb; /* blue-600 */
  text-decoration: none;
}

blockquote {
  margin: 10pt 0;
  padding: 8pt 10pt;
  border-left: 4px solid #60a5fa; /* blue-400 */
  background: #eff6ff; /* blue-50 */
  color: #1f2937; /* gray-800 */
}

hr {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 14pt 0;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 10pt;
  background: #e5e7eb; /* gray-200 (more contrast on white) */
  color: #0f172a; /* slate-900 */
  padding: 1pt 3pt;
  border-radius: 4pt;
}

pre {
  background: #f3f4f6; /* gray-100 */
  color: #0f172a; /* slate-900 */
  padding: 10pt 12pt;
  border-radius: 8pt;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}
pre code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  color: inherit;
  font-size: 9.5pt;
}

table {
  border-collapse: collapse;
  margin: 10pt 0;
  width: 100%;
}
th, td {
  border: 1px solid #e5e7eb;
  padding: 6pt 8pt;
  vertical-align: top;
}
th {
  background: #f9fafb; /* gray-50 */
  color: #111827;
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
