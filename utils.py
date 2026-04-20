from fpdf import FPDF


def clean_text(text):
    """Remove problematic characters for PDF rendering"""
    if not isinstance(text, str):
        return str(text)

    # Remove emojis / unsupported unicode
    return text.encode("latin-1", "ignore").decode("latin-1")


def generate_pdf_bytes(result: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=11)

    # -------------------------
    # HEADER
    # -------------------------
    pdf.cell(0, 10, "Compliance Report", ln=True)

    pdf.ln(5)

    # -------------------------
    # SUMMARY
    # -------------------------
    pdf.multi_cell(0, 8, clean_text(f"Document: {result.get('document_name','')}"))
    pdf.multi_cell(0, 8, clean_text(f"Overall status: {result.get('overall_status','Unknown')}"))
    pdf.multi_cell(0, 8, clean_text(f"Summary: {result.get('summary','')}"))

    pdf.ln(5)

    # -------------------------
    # ISSUES
    # -------------------------
    pdf.cell(0, 8, "Findings:", ln=True)

    for issue in result.get("issues", []):
        pdf.ln(2)

        pdf.multi_cell(0, 8, clean_text(f"Title: {issue.get('title','')}"))
        pdf.multi_cell(0, 8, clean_text(f"Severity: {issue.get('severity','')}"))
        pdf.multi_cell(0, 8, clean_text(f"Why it matters: {issue.get('why_it_matters','')}"))
        pdf.multi_cell(0, 8, clean_text(f"Recommendation: {issue.get('recommendation','')}"))
        pdf.multi_cell(0, 8, clean_text(f"Evidence: {issue.get('evidence','')}"))

        pdf.ln(3)

    # -------------------------
    # STRENGTHS
    # -------------------------
    if result.get("strengths"):
        pdf.cell(0, 8, "Strengths:", ln=True)

        for s in result["strengths"]:
            pdf.multi_cell(0, 8, clean_text(f"- {s}"))

    # -------------------------
    # OUTPUT
    # -------------------------
    return pdf.output(dest="S").encode("latin-1")
