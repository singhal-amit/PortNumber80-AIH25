# 📑 **Challenge 1b: Multi-Collection PDF Analysis**

## 🚀 **Overview**

A semantic PDF analysis pipeline that processes multiple document collections using **persona-driven tasks** to extract only the most relevant sections from large documents.

Supports scenarios like:

- ✈️ **Travel Planning**
- 🧾 **HR & Compliance**
- 📚 **Education**
- 🍽️ **Corporate Catering**

<details>
<summary><strong>📑 Table of Contents</strong></summary>

- [🏁 Overview](#-overview)  
- [🧠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [📁 Collections](#-collections)
- [🧩 Key Highlights](#-key-highlights)
- [🐳 Run Locally](#-run-locally)

</details>

## Solution_1b Demo

[demo.webm](https://github.com/user-attachments/assets/dc5264a8-85aa-495e-a88b-c99c49a0d6c2 )

---

## ⚙️ **Tech Stack**

| Layer                 | Tool                    | Purpose                            |
| --------------------- | ----------------------- | ---------------------------------- |
| **Language**          | Python 3.10             | Core scripting                     |
| **Embedding Model**   | `sentence-transformers` | Semantic text embeddings           |
| **PDF Parsing**       | PyMuPDF (`fitz`)        | PDF text extraction                |
| **Similarity Search** | `scikit-learn`          | Cosine similarity for ranking      |
| **Data Handling**     | JSON                    | Structured input/output            |
| **Containerization**  | Docker                  | Portable, reproducible environment |
| **Persona Store**     | `persona.json`          | Persona-specific keywords          |

---

## 3️⃣ Technical Approach

### ✅ **Key Steps**

---

### 📄 **Text Extraction**

* Uses **PyMuPDF** to extract text **page-by-page** from each PDF.
* Splits text into logical **sections and paragraphs** for fine-grained ranking.

---

### 🧠 **Embeddings & Similarity**

* Runs **SentenceTransformer** with a **local embedding model** (`all-MiniLM`).
* Encodes the **persona role + job task + extracted sections** as embeddings.

---

### 📈 **Relevance Ranking**

* Computes **cosine similarity** between the **job embedding** and **section embeddings**.
* Adjusts final scores with **persona-specific keywords** for better context alignment.

---

### 📑 **Output Generation**

* Saves the **top-ranked sections** in a structured **JSON** format.
* Includes full **metadata**: source document name, page number, section title, and importance rank.

---

### 🐳 **Containerization**

* Uses **Docker** to ensure a **consistent runtime** across development and deployment.
* All **models and code** run **offline** inside the container — no internet needed.

---

## 🗂️ **Project Structure**

```
└── 📁 Solution_1b/                              # Challenge 1b: Multi-Collection PDF Analysis
    ├── 📄 Dockerfile                                   # Container configuration
    ├── 📄 README.md                                    # Solution 1b documentation
    ├── 📄 requirements.txt                             # Python dependencies
    │
    ├── 📁 Collection_1/                                # Travel Planning Collection
    │   ├── 📄 challenge1b_input.json                                 # Input configuration
    │   ├── 📄 challenge1b_output.json                                # Expected result
    │   ├── 📄 solution1b_output.json                                 # Generated JSON
    │   └── 📁 PDFs/                                                  # South of France travel guides
    │
    ├── 📁 Collection_2/                                # Adobe Acrobat Learning Collection
    │   ├── 📄 challenge1b_input.json                                 # Input configuration
    │   ├── 📄 challenge1b_output.json                                # Expected result
    │   ├── 📄 solution1b_output.json                                 # Generated JSON
    │   └── 📁 PDFs/                                                  # Acrobat tutorial documents
    │
    ├── 📁 Collection_3/                                # Recipe Collection
    │   ├── 📄 challenge1b_input.json                                 # Input configuration
    │   ├── 📄 challenge1b_output.json                                # Expected result
    │   ├── 📄 solution1b_output.json                                 # Generated JSON
    │   └── 📁 PDFs/                                                  # Cooking and recipe guides
    │
    └── 📁 src/                                         # Source code for Solution 1b
        ├── 📄 app.py                                                 # Main application logic
        ├── 📄 utils.py                                               # Utility functions
        ├── 📄 persona.json                                           # Persona definitions & learned keywords
        └── 📁 local_model/                                           # Local semantic embedding model  
```

---

## 📁 **Collections**

### ✅ **Collection 1: Travel Planning**

- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to the South of France
- **Documents**: Travel guides

### ✅ **Collection 2: Adobe Acrobat Learning**

- **Persona**: HR Professional
- **Task**: Design & manage onboarding and compliance forms
- **Documents**: Acrobat user manuals

### ✅ **Collection 3: Recipe Collection**

- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet dinner menu for corporate event
- **Documents**: Cooking & catering guides

---

## 🧾 **Input JSON Example**

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_001",
    "test_case_name": "travel_plan"
  },
  "documents": [
    { "filename": "guide1.pdf", "title": "South France Travel Guide" }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan the itinerary for a group trip."
  }
}
```

---

## ✅ **Expected Output: `solution1b_output.json`**

```json
{
  "metadata": {
    "input_documents": ["guide1.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan the itinerary for a group trip.",
    "processing_timestamp": "2025-07-27T12:00:00Z"
  },
  "extracted_sections": [
    {
      "document": "guide1.pdf",
      "section_title": "4-Day Itinerary Highlights",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "guide1.pdf",
      "refined_text": "Details about hotels, transport, sightseeing...",
      "page_number": 3
    }
  ]
}
```

---

## 🧩 **Key Highlights**

* [x] Persona-driven section ranking
* [x] Semantic similarity for precise matching
* [x] JSON output for easy integration
* [x] Same logic works in Docker or virtualenv
---

## 🐳 **Run Locally**

```bash
# Inside virtualenv
cd src
python app.py
```

## 🐳 **Run with Docker**
Build the image:

```bash
docker build -t persona-doc-intel:v8 .
```

Run the container:

```bash
docker run --rm -it -v ${PWD}/Collection_1:/app/Collection_1 -v ${PWD}/Collection_2:/app/Collection_2 -v ${PWD}/Collection_3:/app/Collection_3 persona-doc-intel:v8
```

✅ Outputs are saved back as `solution1b_output.json` in each collection folder.

---

## 👥 **Team PortNumber80**

| GitHub                                                                                                                              | Name             | Role                                              |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------- |
| <a href="https://github.com/gkjha2772"><img src="https://avatars.githubusercontent.com/u/151064648?v=4&s=100" width="50"/></a>      | Gautam Kumar Jha | • Built Solution 1b                               |
| <a href="https://github.com/amit712singhal"><img src="https://avatars.githubusercontent.com/u/123376849?v=4&s=100" width="50"/></a> | Amit Singhal     | • Built Solution 1a                               |
