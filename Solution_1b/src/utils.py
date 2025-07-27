import fitz  # PyMuPDF
import re
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once globally
MODEL = SentenceTransformer("./local_model")

def extract_text_from_pdfs(pdf_folder, docs):
    sections = []
    for doc in docs:
        pdf_path = os.path.join(pdf_folder, doc["filename"])
        pdf = fitz.open(pdf_path)
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text = page.get_text()
            # Split by headings: naive split
            splits = re.split(r'\n(?=[A-Z][^\n]{3,})', text)
            for part in splits:
                if len(part.strip()) > 200:
                    sections.append({
                        "document": doc["filename"],
                        "page_number": page_num + 1,
                        "section_title": part.split('\n')[0].strip(),
                        "text": part.strip()
                    })
    return sections

def embed_texts(texts):
    return MODEL.encode(texts)

def rank_sections(sections, section_embeddings, task_embedding, top_k=10, top_per_doc=3):
    sims = cosine_similarity([task_embedding], section_embeddings)[0]

    # Attach similarity score
    scored_sections = []
    for sec, sim in zip(sections, sims):
        sec_copy = sec.copy()
        sec_copy["score"] = sim
        scored_sections.append(sec_copy)

    # Group by document
    doc_groups = {}
    for sec in scored_sections:
        doc = sec["document"]
        doc_groups.setdefault(doc, []).append(sec)

    # Pick top per document
    top_sections = []
    for secs in doc_groups.values():
        top_in_doc = sorted(secs, key=lambda x: x["score"], reverse=True)[:top_per_doc]
        top_sections.extend(top_in_doc)

    # Combine and pick top overall
    top_sections = sorted(top_sections, key=lambda x: x["score"], reverse=True)[:top_k]

    return top_sections

def refine_subsections(ranked_sections):
    refined = []
    for sec in ranked_sections:
        paragraphs = sec["text"].split("\n\n")
        for p in paragraphs:
            if len(p.split()) > 20:
                refined.append({
                    "document": sec["document"],
                    "refined_text": p.strip(),
                    "page_number": sec["page_number"]
                })
                break  # Take only the first good paragraph
    return refined
