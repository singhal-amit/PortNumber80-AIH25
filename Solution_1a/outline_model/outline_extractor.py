import fitz
import numpy as np
from .clustering import cluster_font_attributes
from .language_cues import detect_headings_by_language
from .model_utils import layout_model_headings

class OutlineExtractor:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.layout_model = self._load_layout_model(model_path) if model_path else None

    def _load_layout_model(self, model_path):
        # Stub for actual layout model (e.g., LayoutLMv3)
        return None

    def extract_outline(self, pdf_path):
        doc = fitz.open(pdf_path)
        font_data = []
        all_lines = []

        for pno, page in enumerate(doc):
            blocks = page.get_text("dict")['blocks']
            for b in blocks:
                if "lines" not in b:
                    continue
                for line in b["lines"]:
                    line_text = " ".join([s["text"] for s in line["spans"]]).strip()
                    if not line_text:
                        continue
                    font_sizes = [s["size"] for s in line["spans"]]
                    is_bold = any(s["flags"] & 2 for s in line["spans"])
                    left = min(s["origin"][0] for s in line["spans"])
                    font_data.append([np.mean(font_sizes), int(is_bold), left])
                    all_lines.append({
                        "text": line_text,
                        "page": pno + 1,
                        "font_size": np.mean(font_sizes),
                        "is_bold": is_bold,
                        "left": left
                    })

        if not font_data:
            return {"title": "Untitled Document", "outline": []}

        heading_labels = cluster_font_attributes(np.array(font_data))
        language_headings = detect_headings_by_language([l["text"] for l in all_lines])
        layout_headings = layout_model_headings(doc, self.layout_model) if self.layout_model else []

        outline = []
        for idx, line in enumerate(all_lines):
            if heading_labels[idx] > 0 or line["text"] in language_headings:
                outline.append({
                    "level": f"H{heading_labels[idx]+1}",
                    "text": line["text"],
                    "page": line["page"]
                })

        outline.extend(layout_headings)
        title = self.extract_title(doc)
        return {"title": title, "outline": outline}

    def extract_title(self, doc):
        first = doc[0]
        blocks = first.get_text("dict")["blocks"]
        max_size = 0
        title = ""
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    if span["size"] >= max_size:
                        max_size = span["size"]
                        title = span["text"].strip()
        return title or "Untitled Document"
