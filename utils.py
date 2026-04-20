import io
from fpdf import FPDF

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    # Replace smart quotes and common unicode punctuation
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2026": "...",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "ignore").decode("latin-1")

def section_header(pdf, W, text):
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(W, 8, text, ln=True)
    pdf.set_font("Arial", size=11)
    pdf.ln(1)

def labeled_block(pdf, W, label, value):
    pdf.set_font("Arial", style="B", size=11)
    pdf.multi_cell(W, 7, clean_text(label))
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(W, 7, clean_text(value))
    pdf.ln(1)

def generate_pdf_bytes(result: dict) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    W = pdf.w - 40  # 170mm usable width

    # -------------------------
    # HEADER
    # -------------------------
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(W, 10, "Compliance Report", ln=True)
    pdf.ln(3)

    # -------------------------
    # SUMMARY
    # -------------------------
    section_header(pdf, W, "Summary")
    labeled_block(pdf, W, "Document:", result.get("document_name", ""))
    labeled_block(pdf, W, "Overall Status:", result.get("overall_status", "Unknown"))
    labeled_block(pdf, W, "Summary:", result.get("summary", ""))
    pdf.ln(3)

    # -------------------------
    # ISSUES
    # -------------------------
    section_header(pdf, W, "Findings")

    for i, issue in enumerate(result.get("issues", []), start=1):
        pdf.set_font("Arial", style="B", size=11)
        pdf.multi_cell(W, 7, clean_text(f"{i}. {issue.get('title', '')}"))
        pdf.set_font("Arial", size=11)
        labeled_block(pdf, W, "Severity:", issue.get("severity", ""))
        labeled_block(pdf, W, "Why it matters:", issue.get("why_it_matters", ""))
        labeled_block(pdf, W, "Recommendation:", issue.get("recommendation", ""))
        labeled_block(pdf, W, "Evidence:", issue.get("evidence", "Not found"))
        pdf.ln(4)

    # -------------------------
    # STRENGTHS
    # -------------------------
    if result.get("strengths"):
        section_header(pdf, W, "What the Document Does Well")
        for s in result["strengths"]:
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(W, 7, clean_text(f"- {s}"))
        pdf.ln(3)

    # -------------------------
    # RULES CONSIDERED
    # -------------------------
    if result.get("rules_considered"):
        section_header(pdf, W, "Rules Considered")
        for rule in result["rules_considered"]:
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(W, 7, clean_text(f"- {rule.get('id','')}: {rule.get('title','')}"))

    # -------------------------
    # OUTPUT
    # -------------------------
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
