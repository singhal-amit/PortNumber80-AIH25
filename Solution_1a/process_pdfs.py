import json
from pathlib import Path
from pdf_outliner.extractor import PDFOutlineExtractor
from tests.test_solution import compare_outputs

def main():
    INPUT_DIR = Path("sample_dataset/pdfs")
    OUTPUT_DIR = Path("sample_dataset/outputs")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    extractor = PDFOutlineExtractor()
    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    print(f"\n📂 Found {len(pdf_files)} PDF file(s) to process\n{'-' * 50}")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"📄 [{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        result = extractor.process_pdf(pdf_file)

        output_path = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"   ├─ 🏷️  Title:   {result['title']}")
        print(f"   └─ 📑 Headings: {len(result['outline'])}\n")

    print("🧪 Testing PDF Processing Solution")
    print("=" * 50)

    current_dir = Path(".")

    checks = {
        "process_pdfs.py": current_dir / "process_pdfs.py",
        "Dockerfile": current_dir / "Dockerfile",             # adjust if not used
        "requirements.txt": current_dir / "requirements.txt"
    }

    for name, path in checks.items():
        if not path.exists():
            print(f"❌ {name} not found")
            return 1
        print(f"✅ {name} found")

    if compare_outputs():
        print("\n🎉 All tests passed! Solution is ready for submission.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    main()
