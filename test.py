import json
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ---------------- LOAD JSON ----------------
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- UTILS ----------------
def map_striver_diff(val):
    return {0: "Easy", 1: "Medium", 2: "Hard"}.get(val, "Unknown")

def extract_striver_questions(data):
    """Extract Striver-style questions from the provided JSON data.

    Supports two input layouts:
    1) Current file layout (root is a list):
       [ { step_no, step_title, sub_steps: [ { topics: [ { question_title, editorial_link, lc_link, difficulty } ] } ] } ]

    2) Legacy layout (root is a dict with 'sheetData' key):
       { sheetData: [ { topics: [ { title, lc_link, difficulty } ] } ] }
    """
    striver_questions = []

    # Case 1: Root is a list of steps (current data.json format)
    if isinstance(data, list):
        for step in data:
            sub_steps = step.get("sub_steps", []) if isinstance(step, dict) else []
            for sub in sub_steps:
                topics = sub.get("topics", []) if isinstance(sub, dict) else []
                for t in topics:
                    if not isinstance(t, dict):
                        continue
                    striver_questions.append({
                        "title": t.get("question_title") or t.get("title"),
                        "difficulty": map_striver_diff(t.get("difficulty", 0)),
                        "topic": None,  # no topic in this dataset; will fill later if needed
                        "lc_url": t.get("lc_link")
                    })

    # Case 2: Legacy dict format with 'sheetData'
    elif isinstance(data, dict):
        for step in data.get("sheetData", []):
            topics = step.get("topics", []) if isinstance(step, dict) else []
            for q in topics:
                if not isinstance(q, dict):
                    continue
                striver_questions.append({
                    "title": q.get("title"),
                    "difficulty": map_striver_diff(q.get("difficulty", 0)),
                    "topic": None,
                    "lc_url": q.get("lc_link")
                })

    return striver_questions

# Note: NeetCode parsing removed per request

# ---------------- BUILD PDF ----------------
def build_pdf(striver_list, output_file="Striver_Questions.pdf"):
    styles = getSampleStyleSheet()
    wrap_style = ParagraphStyle('wrap', parent=styles['Normal'], wordWrap='CJK')
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []

    # Table header
    table_data = [["Topic", "Question", "Difficulty", "Comments / Logic / Design Pattern"]]
    for q in striver_list:
        table_data.append([
            q.get("topic") or "",
            Paragraph(q.get("title") or "", wrap_style),
            q.get("difficulty") or "",
            ""
        ])

    table = Table(table_data, colWidths=[160, 260, 90, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Copyright
    elements.append(Paragraph(
        "© Striver SDE Sheet (TakeUForward) and NeetCode.io. "
        "Question titles and difficulties are used for educational purposes only.",
        styles["Italic"]
    ))

    doc.build(elements)
    print(f"✅ PDF generated: {output_file}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    striver_data = load_json("data.json")
    striver_qs = extract_striver_questions(striver_data)
    build_pdf(striver_qs)
