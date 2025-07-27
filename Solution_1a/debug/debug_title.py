import fitz

def debug_title_detection(pdf_path):
    """Debug title detection for a specific PDF"""
    doc = fitz.open(pdf_path)
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]
    
    print(f"\n=== DEBUGGING TITLE DETECTION FOR {pdf_path} ===")
    text_elements = []
    
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            max_size = 0
            line_y = line["bbox"][1]
            page_height = first_page.rect.height
            if line_y < page_height * 0.10 or line_y > page_height * 0.90:
                continue
            for span in line["spans"]:
                text = span["text"].strip()
                if text:
                    line_text += text + " "
                    max_size = max(max_size, span["size"])
            line_text = line_text.strip()
            if 8 <= len(line_text) <= 200:
                text_elements.append({
                    "text": line_text,
                    "size": max_size,
                    "position": line_y,
                    "is_bold": any(s["flags"] & 2**4 for s in line["spans"])
                })

    text_elements.sort(key=lambda x: (-x["size"], x["position"]))

    print("Top 10 text elements by size:")
    for i, element in enumerate(text_elements[:10]):
        print(f"  {i+1}. Size:{element['size']:.1f} Bold:{element['is_bold']} | {element['text']}")
    doc.close()

# Sample files to debug
if __name__ == "__main__":
    debug_title_detection("./sample_dataset/pdfs/file01.pdf")
    debug_title_detection("./sample_dataset/pdfs/file02.pdf")
    debug_title_detection("./sample_dataset/pdfs/file03.pdf")
    debug_title_detection("./sample_dataset/pdfs/file04.pdf")
    debug_title_detection("./sample_dataset/pdfs/file05.pdf")
