import io
from fpdf import FPDF

def clean_text(text):
    """Remove problematic characters for PDF rendering"""
    if not isinstance(text, str):
        text = str(text)
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_pdf_bytes(result: dict) -> bytes:
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    W = 180

    # -------------------------
    # HEADER
    # -------------------------
    pdf.set_font("Arial", style="B", size=13)
    pdf.cell(W, 10, "Compliance Report", ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", size=11)

    # -------------------------
    # SUMMARY
    # -------------------------
    pdf.multi_cell(W, 8, clean_text(f"Document: {result.get('document_name','')}"))
    pdf.multi_cell(W, 8, clean_text(f"Overall status: {result.get('overall_status','Unknown')}"))
    pdf.multi_cell(W, 8, clean_text(f"Summary: {result.get('summary','')}"))
    pdf.ln(5)

    # -------------------------
    # ISSUES
    # -------------------------
    pdf.set_font("Arial", style="B", size=11)
    pdf.cell(W, 8, "Findings:", ln=True)
    pdf.set_font("Arial", size=11)

    for issue in result.get("issues", []):
        pdf.ln(2)
        pdf.multi_cell(W, 8, clean_text(f"Title: {issue.get('title','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Severity: {issue.get('severity','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Why it matters: {issue.get('why_it_matters','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Recommendation: {issue.get('recommendation','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Evidence: {issue.get('evidence','')}"))
        pdf.ln(3)

    # -------------------------
    # STRENGTHS
    # -------------------------
    if result.get("strengths"):
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(W, 8, "Strengths:", ln=True)
        pdf.set_font("Arial", size=11)
        for s in result["strengths"]:
            pdf.multi_cell(W, 8, clean_text(f"- {s}"))

    # -------------------------
    # RULES CONSIDERED
    # -------------------------
    if result.get("rules_considered"):
        pdf.ln(4)
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(W, 8, "Rules Considered:", ln=True)
        pdf.set_font("Arial", size=11)
        for rule in result["rules_considered"]:
            pdf.multi_cell(W, 8, clean_text(f"- {rule.get('id','')}: {rule.get('title','')}"))

    # -------------------------
    # OUTPUT
    # -------------------------
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
