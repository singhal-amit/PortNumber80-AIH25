import json
import os
from datetime import datetime
from utils import extract_text_from_pdfs, embed_texts, rank_sections, refine_subsections

# 📁 List your collections here
COLLECTIONS = [
    "./Collection_1/",
    "./Collection_2/",
    "./Collection_3/"
]

for COLLECTION_PATH in COLLECTIONS:
    PDF_PATH = os.path.join(COLLECTION_PATH, "PDFs/")
    INPUT_JSON = os.path.join(COLLECTION_PATH, "challenge1b_input.json")

    # Make output name dynamic per collection
    collection_name = os.path.basename(os.path.normpath(COLLECTION_PATH))
    OUTPUT_JSON = os.path.join("./src/output/", f"{collection_name}_Output.json")

    # Load input
    with open(INPUT_JSON) as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]

    print(f"\n🚀 Processing: {collection_name}")

    # 1️⃣ Extract PDF text
    sections = extract_text_from_pdfs(PDF_PATH, input_data["documents"])

    # 2️⃣ Embed persona+job
    task_embedding = embed_texts([persona + " " + job])[0]

    # 3️⃣ Embed sections
    section_texts = [s["text"] for s in sections]
    section_embeddings = embed_texts(section_texts)

    # 4️⃣ Rank sections
    ranked_sections = rank_sections(sections, section_embeddings, task_embedding)

    # 5️⃣ Refine subsections
    subsections = refine_subsections(ranked_sections)

    # 6️⃣ Prepare output
    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in input_data["documents"]],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": s["document"],
                "section_title": s["section_title"],
                "importance_rank": idx + 1,
                "page_number": s["page_number"]
            }
            for idx, s in enumerate(ranked_sections)
        ],
        "subsection_analysis": subsections
    }

    # 💾 Save output
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=4)

    print(f"✅ Output written to {OUTPUT_JSON}")
