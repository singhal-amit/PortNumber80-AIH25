# 📄 Challenge 1a: PDF Processing Solution

## 🏁 Overview
This repository contains the solution for **Challenge 1a** of the **Adobe India Hackathon 2025**. The objective is to implement a containerized solution that processes PDF documents and extracts structured data into **JSON** format, while adhering to **performance**, **resource**, and **offline** constraints.

<details>
<summary><strong>📑 Table of Contents</strong></summary>

- [🏁 Overview](#-overview)  
- [🧠 Tech Stack](#-tech-stack)
- [⚙️ Installation & Running](#️-installation--running)
- [🧪 Testing the Solution](#-testing-the-solution)
- [📁 Project Structure](#-project-structure)
- [📌 Implementation Details](#-implementation)
- [📋 Validation Checklist](#-validation-checklist)

</details>

## Solution_1a Demo

[!solution1a_demo.mp4](https://github.com/user-attachments/assets/ce1a6c98-7159-4197-acea-54de93998d99)

---

## 🧠 Tech Stack

| 🔧 Component       | 💻 Technology Used                                      | 🔍 Purpose                                |
|-------------------|---------------------------------------------------------|-------------------------------------------|
| 🐍 **Language**    | ![Python](https://img.shields.io/badge/Python-3.11-blue) | Core development language                  |
| 📄 **PDF Parsing** | `PyMuPDF`, `pdfplumber`                                | Extract text, layout, and metadata         |
| 🤖 **ML Framework**| `Transformers` (HuggingFace)                           | Language modeling and heading detection    |
| 🧠 **Model**       | `BERT-tiny` (local)                                    | Lightweight model for classification       |
| 🐳 **Container**   | `Docker`                                               | Containerization of the solution           |
| 🧪 **Testing**     | `pytest`                                               | Test suite for validation and regression   |
| 📦 **Utilities**   | `tqdm`, `scikit-learn`, `argparse`                     | Progress bar, clustering, CLI parsing      |

---

## ⚙️ Installation & Running

```bash
# Clone the repository
git clone https://github.com/singhal-amit/PortNumber80-AIH25.git
cd PortNumber80-AIH25

# Build and start the container (Docker Compose)
docker compose build
docker compose up
````

---

## 🧪 Testing the Solution

### 🐞 Debug Individual PDFs

```bash
# Navigate into Solution_1a
cd Solution_1a

# Debug PDF layout and structure
python debug/debug_pdf.py

# Debug title and heading extraction logic
python debug/debug_title.py
```

### ✅ Run Test Suite

```bash
# Run test suite from Solution_1a
python tests/test_solution.py
```

---

## 📁 Project Structure

```
📁 Solution_1a/
├── 📄 Dockerfile                   # Container config
├── 📄 process_pdfs.py              # Main script for processing PDFs
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 debug/                       # Debug scripts
│   ├── 🐞 debug_pdf.py
│   └── 🐞 debug_title.py
│
├── 📁 local_model/                 # Offline transformer model (BERT-tiny)
│   └── 📁 models--prajjwal1--bert-tiny/
│
├── 📁 pdf_outliner/                # PDF outline extraction logic
│   └── 📄 extractor.py
│
├── 📁 sample_dataset/              # Dataset for evaluation
│   ├── 📁 expected_outputs/        # Provided expected JSON
│   ├── 📁 outputs/                 # Our generated output
│   ├── 📁 pdfs/                    # Input PDF files
│   └── 📁 schema/                  # JSON schema
│       └── 📄 output_schema.json
│
└── 📁 tests/
    └── 📄 test_solution.py         # Unit tests
```

---

## 📌 Implementation

### Solution Overview

The provided `process_pdfs.py` script is a starting point that:

* Scans the input directory for PDF files
* Uses rule-based + ML techniques to extract structure
* Generates `filename.json` for every `filename.pdf`

### Performance Guidelines

* ⚙️ Efficient use of **CPU (8 cores)** and **RAM (≤16 GB)**
* ⏱️ Processing should complete within **10 seconds** for 50-page documents
* 🌐 Fully **offline** and **network-isolated**
* 🧠 ML model is **< 200MB**, locally available

### Testing Guidelines

* Covers **simple**, **complex**, and **large** PDFs
* Validates format against schema
* Includes **unit tests** and **debug utilities**

---

## 📋 Validation Checklist

### ✅ Core Requirements

* [x] Process all PDFs in input directory
* [x] Generate structured JSON output for each PDF
* [x] Match output format with schema (`output_schema.json`)
* [x] Entirely offline: No internet access required
* [x] All dependencies and models are open source

### ✅ Performance & Constraints

* [x] Complete 50-page PDF processing < 10s
* [x] ≤ 16GB RAM usage
* [x] ML model ≤ 200MB
* [x] Efficient CPU usage (8 cores)
* [x] AMD64 compatibility

### ✅ Docker Requirements

* [x] Functional `Dockerfile`
* [x] Works with `--platform linux/amd64`
* [x] Read-only input mount
* [x] Writable output mount
* [x] `--network none` enforced

### ✅ Code Quality & Testing

* [x] Well-structured code and modular design
* [x] All dependencies in `requirements.txt`
* [x] Unit tests implemented and passing
* [x] Debug scripts available
* [x] Meaningful error handling and logging

---
