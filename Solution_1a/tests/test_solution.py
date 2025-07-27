#!/usr/bin/env python3
"""
Test script to verify the PDF processing solution works correctly.
"""

import json
import sys
from pathlib import Path

def compare_outputs():
    """Compare generated outputs with expected outputs"""
    
    expected_dir = Path("./sample_dataset/expected_outputs")
    generated_dir = Path("./sample_dataset/outputs")
    
    if not expected_dir.exists():
        print("❌ Expected outputs directory not found")
        return False
    if not generated_dir.exists():
        print("❌ Generated outputs directory not found")
        return False

    expected_files = list(expected_dir.glob("*.json"))
    if not expected_files:
        print("❌ No expected JSON files found")
        return False

    print(f"✅ Found {len(expected_files)} expected output files")

    all_good = True
    for expected_file in expected_files:
        print(f"\n📄 Checking {expected_file.name}...")

        generated_file = generated_dir / expected_file.name
        if not generated_file.exists():
            print(f"  ❌ Output file {generated_file.name} is missing")
            all_good = False
            continue

        try:
            with open(generated_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "title" not in data:
                print("  ❌ Missing 'title' field")
                all_good = False
            else:
                print(f"  ✅ Title: '{data['title']}'")

            if "outline" not in data:
                print("  ❌ Missing 'outline' field")
                all_good = False
            else:
                print(f"  ✅ Outline: {len(data['outline'])} headings")

                for i, heading in enumerate(data["outline"]):
                    if not all(k in heading for k in ("text", "page", "level")):
                        print(f"  ❌ Heading {i} missing fields")
                        all_good = False
                        break
                    if heading["level"] not in ("H1", "H2", "H3", "H4"):
                        print(f"  ❌ Invalid level: {heading['level']}")
                        all_good = False
                        break
                    if not isinstance(heading["page"], int):
                        print(f"  ❌ Invalid page number: {heading['page']}")
                        all_good = False
                        break
                else:
                    print("  ✅ All headings are valid")

        except json.JSONDecodeError as e:
            print(f"  ❌ Invalid JSON: {e}")
            all_good = False
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            all_good = False

    return all_good

def main():
    print("🧪 Testing PDF Processing Solution")
    print("=" * 50)

    current_dir = Path(".")
    parent_dir = Path("..")

    checks = {
        "process_pdfs.py": current_dir / "process_pdfs.py",
        "Dockerfile": current_dir / "Dockerfile",             # adjust if not used
        "requirements.txt": parent_dir / "requirements.txt"
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
    sys.exit(main())
