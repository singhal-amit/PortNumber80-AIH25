import fitz
from pathlib import Path

def debug_title_detection(pdf_path):
    """Debug title detection for a specific PDF"""
    doc = fitz.open(pdf_path)
    pdf_name = Path(pdf_path).name
    print(f"\n\n📘 === Debugging Title Detection: {pdf_name} ===")

    first_page = doc[0]
    page_height = first_page.rect.height
    blocks = first_page.get_text("dict")["blocks"]
    text_elements = []

    for block in blocks:
        if "lines" not in block:
            continue

        for line in block["lines"]:
            line_y = line["bbox"][1]
            if line_y < page_height * 0.10 or line_y > page_height * 0.90:
                continue  # Skip headers/footers

            line_text = ""
            max_size = 0
            is_bold = False

            for span in line["spans"]:
                text = span["text"].strip()
                if not text:
                    continue
                line_text += text + " "
                max_size = max(max_size, span["size"])
                is_bold = is_bold or bool(span["flags"] & 2**4)

            line_text = line_text.strip()
            if 8 <= len(line_text) <= 200:
                text_elements.append({
                    "text": line_text,
                    "size": max_size,
                    "position": line_y,
                    "is_bold": is_bold
                })

    doc.close()

    if not text_elements:
        print("⚠️ No valid text elements found on the first page.")
        return

    # Sort by font size (desc) then vertical position (top to bottom)
    text_elements.sort(key=lambda x: (-x["size"], x["position"]))

    print("\n🔝 Top 10 title candidates by font size:")
    print("────────────────────────────────────────────")
    for i, el in enumerate(text_elements[:10]):
        print(f"{i+1:>2}. Size: {el['size']:.1f} | Bold: {el['is_bold']} | Text: {el['text']}")


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
            debug_title_detection(pdf)
        else:
            print(f"⚠️ File not found: {pdf}")
