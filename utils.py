from fpdf import FPDF

def generate_pdf_bytes(result: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Fire Extinguisher Compliance Report", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"Document: {result.get('document_name','Unknown')}")
    pdf.multi_cell(0, 8, f"Overall status: {result.get('overall_status','Unknown')}")
    pdf.ln(2)
    pdf.multi_cell(0, 8, f"Summary: {result.get('summary','')}")

    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Findings", ln=True)

    pdf.set_font("Arial", size=11)
    issues = result.get("issues", [])
    if not issues:
        pdf.multi_cell(0, 8, "No major issues were flagged for the scoped rule set.")
    else:
        for idx, issue in enumerate(issues, start=1):
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 8, f"{idx}. {issue.get('title','Issue')} ({issue.get('severity','Medium')})")
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, f"Why it matters: {issue.get('why_it_matters','')}")
            pdf.multi_cell(0, 8, f"Recommendation: {issue.get('recommendation','')}")
            pdf.multi_cell(0, 8, f"Evidence: {issue.get('evidence','Not found')}")
            pdf.ln(1)

    strengths = result.get("strengths", [])
    if strengths:
        pdf.ln(2)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Strengths", ln=True)
        pdf.set_font("Arial", size=11)
        for s in strengths:
            pdf.multi_cell(0, 8, f"- {s}")

    pdf.ln(2)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Rules Considered", ln=True)
    pdf.set_font("Arial", size=11)
    for r in result.get("rules_considered", []):
        pdf.multi_cell(0, 8, f"- {r.get('id','')}: {r.get('title','')}")

    return bytes(pdf.output(dest="S"))
