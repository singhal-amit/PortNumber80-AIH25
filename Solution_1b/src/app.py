import json
import os
from datetime import datetime, timezone
from utils import (
    extract_text_from_pdfs,
    embed_texts,
    rank_sections,
    refine_subsections,
    learn_new_keywords
)

# 📁 Collections to process
COLLECTIONS = [
    os.path.join(os.path.dirname(__file__), "../Collection_1/"),
    os.path.join(os.path.dirname(__file__), "../Collection_2/"),
    os.path.join(os.path.dirname(__file__), "../Collection_3/")
]

# ✅ Load persona definitions
PERSONA_FILE =  os.path.join(os.path.dirname(__file__), "persona.json")
with open(PERSONA_FILE) as f:
    PERSONAS = json.load(f)

# ✅ Loop through collections
for COLLECTION_PATH in COLLECTIONS:
    PDF_PATH = os.path.join(COLLECTION_PATH, "PDFs/")
    INPUT_JSON = os.path.join(COLLECTION_PATH, "challenge1b_input.json")

    collection_name = os.path.basename(os.path.normpath(COLLECTION_PATH))
    OUTPUT_JSON = os.path.join(COLLECTION_PATH, f"solution1b_output.json")

    with open(INPUT_JSON) as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"].lower()
    job = input_data["job_to_be_done"]["task"]

    print(f"\n🚀 Processing: {collection_name}")

    # 📄 Extract text
    sections = extract_text_from_pdfs(PDF_PATH, input_data["documents"])

    # 🔍 Embed
    task_embedding = embed_texts([persona + " " + job])[0]
    section_texts = [s["text"] for s in sections]
    section_embeddings = embed_texts(section_texts)

    # 🧩 Get persona keywords
    persona_keywords = PERSONAS.get(persona, {}).get("keywords", [])

    # 🏅 Rank and refine
    ranked_sections = rank_sections(
        sections,
        section_embeddings,
        task_embedding,
        keywords=persona_keywords
    )
    subsections = refine_subsections(ranked_sections)

    # ✅ Build output
    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in input_data["documents"]],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now(timezone.utc).isoformat()
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

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=4)

    print(f"✅ Output written to {OUTPUT_JSON}")

    # 🧠 Learn new keywords!
    PERSONAS = learn_new_keywords(PERSONAS, persona, ranked_sections)

# ✅ Save back updated personas
with open(PERSONA_FILE, "w") as f:
    json.dump({"personas": PERSONAS}, f, indent=4)

print("\n🎉 Updated persona.json with learned keywords!")
