import json
import tempfile
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
CORS(app)

# ---------------- PARSING ----------------
def map_striver_diff(val):
    return {0: "Easy", 1: "Medium", 2: "Hard"}.get(val, "Unknown")


def extract_striver_questions(data):
    """Extract questions from current or legacy JSON format."""
    striver_questions = []

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
                        "topic": None,
                        "lc_url": t.get("lc_link"),
                    })
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
                    "lc_url": q.get("lc_link"),
                })

    return striver_questions


# ---------------- PDF ----------------
def build_pdf(striver_list, output_path):
    styles = getSampleStyleSheet()
    wrap_style = ParagraphStyle('wrap', parent=styles['Normal'], wordWrap='CJK')
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    elements = []
    table_data = [["Topic", "Question", "Difficulty", "Comments / Logic / Design Pattern"]]

    for q in striver_list:
        table_data.append([
            q.get("topic") or "",
            Paragraph(q.get("title") or "", wrap_style),
            q.get("difficulty") or "",
            "",
        ])

    table = Table(table_data, colWidths=[100, 260, 90, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "© Striver SDE Sheet (TakeUForward). Question titles and difficulties are used for educational purposes only.",
        styles["Italic"],
    ))

    doc.build(elements)


# ---------------- API ----------------
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})


@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """Accept JSON via multipart file upload or raw JSON body and return a PDF."""
    try:
        # Priority 1: multipart/form-data with file field 'file'
        if 'file' in request.files:
            data_file = request.files['file']
            data = json.load(data_file.stream)
        else:
            # Priority 2: raw JSON
            data = request.get_json(force=True, silent=False)

        questions = extract_striver_questions(data)

        # Create temp file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
        build_pdf(questions, pdf_path)

        return send_file(pdf_path, as_attachment=True, download_name='Striver_Questions.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)
