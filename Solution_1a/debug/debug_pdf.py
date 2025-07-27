import fitz
from pathlib import Path

def debug_pdf(pdf_path):
    """Debug PDF content to understand structure"""
    doc = fitz.open(pdf_path)
    pdf_name = Path(pdf_path).name
    print(f"\n\n📄 === Debugging: {pdf_name} ===")
    print(f"📄 Total Pages: {len(doc)}")

    for page_num in range(min(3, len(doc))):  # Only first 3 pages
        print(f"\n--- 📄 Page {page_num + 1} ---")
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block_idx, block in enumerate(blocks):
            if "lines" not in block:
                continue

            for line_idx, line in enumerate(block["lines"]):
                line_text = ""
                sizes = []
                bold_flags = []

                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    sizes.append(span["size"])
                    bold_flags.append(bool(span["flags"] & 2**4))  # Bold bit
                    line_text += text + " "

                if not line_text.strip() or len(line_text.strip()) < 4:
                    continue

                avg_size = sum(sizes) / len(sizes) if sizes else 0
                is_bold = any(bold_flags)

                print(f"  ▪️ [{block_idx}:{line_idx}] Size: {avg_size:.1f} | Bold: {is_bold} | Text: {line_text.strip()}")

    doc.close()


if __name__ == "__main__":
    sample_files = [
        "./sample_dataset/pdfs/file01.pdf",
        "./sample_dataset/pdfs/file02.pdf",
        "./sample_dataset/pdfs/file03.pdf",
        "./sample_dataset/pdfs/file04.pdf",
        "./sample_dataset/pdfs/file05.pdf",
    ]

    for pdf in sample_files:
        if Path(pdf).exists():
            debug_pdf(pdf)
        else:
            print(f"⚠️ File not found: {pdf}")
