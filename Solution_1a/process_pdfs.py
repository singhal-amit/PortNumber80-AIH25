import json
from pathlib import Path
from pdf_outliner.extractor import PDFOutlineExtractor

def main():
    INPUT_DIR = Path("sample_dataset/pdfs")
    OUTPUT_DIR = Path("sample_dataset/outputs")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    extractor = PDFOutlineExtractor()
    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    print(f"Processing {len(pdf_files)} PDF files...")
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        result = extractor.process_pdf(pdf_file)

        output_path = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"  Title: '{result['title']}'")
        print(f"  Headings: {len(result['outline'])}")

if __name__ == "__main__":
    main()
