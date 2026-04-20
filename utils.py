import io
from fpdf import FPDF

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_pdf_bytes(result: dict) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Arial", size=11)

    W = pdf.w - 40  # page width minus left+right margins (170mm on A4)

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
    pdf.ln(2)
    pdf.multi_cell(W, 8, clean_text(f"Overall status: {result.get('overall_status','Unknown')}"))
    pdf.ln(2)
    pdf.multi_cell(W, 8, clean_text(f"Summary: {result.get('summary','')}"))
    pdf.ln(5)

    # -------------------------
    # ISSUES
    # -------------------------
    pdf.set_font("Arial", style="B", size=11)
    pdf.cell(W, 8, "Findings:", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", size=11)

    for issue in result.get("issues", []):
        pdf.multi_cell(W, 8, clean_text(f"Title: {issue.get('title','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Severity: {issue.get('severity','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Why it matters: {issue.get('why_it_matters','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Recommendation: {issue.get('recommendation','')}"))
        pdf.multi_cell(W, 8, clean_text(f"Evidence: {issue.get('evidence','')}"))
        pdf.ln(4)

    # -------------------------
    # STRENGTHS
    # -------------------------
    if result.get("strengths"):
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(W, 8, "Strengths:", ln=True)
        pdf.ln(2)
        pdf.set_font("Arial", size=11)
        for s in result["strengths"]:
            pdf.multi_cell(W, 8, clean_text(f"- {s}"))
        pdf.ln(4)

    # -------------------------
    # RULES CONSIDERED
    # -------------------------
    if result.get("rules_considered"):
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(W, 8, "Rules Considered:", ln=True)
        pdf.ln(2)
        pdf.set_font("Arial", size=11)
        for rule in result["rules_considered"]:
            pdf.multi_cell(W, 8, clean_text(f"- {rule.get('id','')}: {rule.get('title','')}"))

    # -------------------------
    # OUTPUT
    # -------------------------
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
