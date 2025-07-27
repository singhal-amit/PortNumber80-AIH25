import os
import json
from outline_model.outline_extractor import OutlineExtractor

INPUT_DIR = os.path.join("sample_dataset", "pdfs")
OUTPUT_DIR = os.path.join("sample_dataset", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

extractor = OutlineExtractor()

def process_all_pdfs():
    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith(".pdf"):
            continue
        pdf_path = os.path.join(INPUT_DIR, fname)
        output_path = os.path.join(OUTPUT_DIR, fname.replace(".pdf", ".json"))

        print(f"📄 Processing: {pdf_path}")
        result = extractor.extract_outline(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✅ Wrote: {output_path}")

if __name__ == "__main__":
    process_all_pdfs()
