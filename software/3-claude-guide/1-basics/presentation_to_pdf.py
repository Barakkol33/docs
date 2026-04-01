"""
Note: this script is a POC and might have some bugs 

Convert an HTML slide presentation to PDF.

Each element with class="slide" becomes a separate page.
Uses Playwright (headless Chromium) to render the slides.

Usage:
    python presentation_to_pdf.py presentation.html -o output.pdf
    python presentation_to_pdf.py presentation.html -o output.pdf --width 1280 --height 720
"""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an HTML presentation to PDF.")
    parser.add_argument("input", type=Path, help="Path to the HTML presentation file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output PDF path (default: <input-stem>.pdf)",
    )
    parser.add_argument("--width", type=int, default=1280, help="Viewport width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Viewport height (default: 720)")
    parser.add_argument(
        "--wait", type=float, default=0.5,
        help="Seconds to wait after activating each slide for animations (default: 0.5)",
    )
    args = parser.parse_args()

    input_file: Path = args.input.resolve()
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")

    output_file = args.output if args.output else Path(f"{input_file.stem}.pdf")

    file_url = input_file.as_uri()
    wait_ms = int(args.wait * 1000)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(file_url, wait_until="networkidle")

        # Wait for fonts to load
        page.wait_for_timeout(1500)

        # Count slides
        slide_count = page.eval_on_selector_all(".slide", "els => els.length")
        if slide_count == 0:
            raise SystemExit("No elements with class='slide' found in the HTML file.")

        print(f"Found {slide_count} slides. Rendering...")

        # Hide UI chrome but keep animations running (we'll wait for them)
        page.evaluate("""() => {
            const hideSelectors = ['.nav', '.slide-counter', '#counter', '.cursor',
                                   '.cursor-dot', '.slide-dots', '.progress', '.progress-bar'];
            hideSelectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
            });
        }""")

        screenshots = []

        for i in range(slide_count):
            # Activate only the current slide
            page.evaluate("""(idx) => {
                document.querySelectorAll('.slide').forEach((s, j) => {
                    if (j === idx) {
                        s.style.display = 'flex';
                        s.classList.add('active');
                    } else {
                        s.style.display = 'none';
                        s.classList.remove('active');
                    }
                });
            }""", i)

            # Wait for staggered animations to complete
            page.wait_for_timeout(wait_ms)

            screenshot = page.screenshot(full_page=False)
            screenshots.append(screenshot)
            print(f"  Slide {i + 1}/{slide_count} captured")

        browser.close()

    # Build PDF from screenshots using PyMuPDF
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise SystemExit("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")

    merged = fitz.open()
    for screenshot in screenshots:
        img = fitz.open(stream=screenshot, filetype="png")
        # Create a page matching the image dimensions (in points: 72 dpi)
        pix = fitz.Pixmap(screenshot)
        page_width = pix.width * 72 / 96  # convert px to pt (assuming 96 dpi screen)
        page_height = pix.height * 72 / 96
        pdf_page = merged.new_page(width=page_width, height=page_height)
        pdf_page.insert_image(fitz.Rect(0, 0, page_width, page_height), stream=screenshot)

    merged.save(str(output_file))
    merged.close()

    print(f"Saved {slide_count}-page PDF to: {output_file}")


if __name__ == "__main__":
    main()
