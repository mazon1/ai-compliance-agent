import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2026": "...",
        "&": "&amp;", "<": "&lt;", ">": "&gt;",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def generate_pdf_bytes(result: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=16, spaceAfter=6)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=4, spaceBefore=10)
    h3_style = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=11, spaceAfter=2, spaceBefore=6)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, spaceAfter=4, leading=14)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=10, spaceAfter=3, leftIndent=10, leading=14)
    severity_colors = {"high": colors.HexColor("#c0392b"), "medium": colors.HexColor("#e67e22"), "low": colors.HexColor("#27ae60")}

    # HEADER
    story.append(Paragraph("Compliance Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 6))

    # SUMMARY
    story.append(Paragraph("Summary", h2_style))
    story.append(Paragraph(f"<b>Document:</b> {clean_text(result.get('document_name',''))}", body_style))
    story.append(Paragraph(f"<b>Overall Status:</b> {clean_text(result.get('overall_status','Unknown'))}", body_style))
    story.append(Paragraph(f"<b>Summary:</b> {clean_text(result.get('summary',''))}", body_style))
    story.append(Spacer(1, 6))

    # FINDINGS
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Paragraph("Findings", h2_style))

    for i, issue in enumerate(result.get("issues", []), start=1):
        sev = issue.get("severity", "")
        sev_color = severity_colors.get(sev.lower(), colors.black)
        sev_style = ParagraphStyle("Sev", parent=body_style, textColor=sev_color, fontName="Helvetica-Bold")

        story.append(Paragraph(f"{i}. {clean_text(issue.get('title',''))}", h3_style))
        story.append(Paragraph(f"Severity: {clean_text(sev)}", sev_style))
        story.append(Paragraph(f"<b>Why it matters:</b> {clean_text(issue.get('why_it_matters',''))}", body_style))
        story.append(Paragraph(f"<b>Recommendation:</b> {clean_text(issue.get('recommendation',''))}", body_style))
        story.append(Paragraph(f"<b>Evidence:</b> <i>{clean_text(issue.get('evidence','Not found'))}</i>", body_style))
        story.append(Spacer(1, 4))

    # STRENGTHS
    if result.get("strengths"):
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        story.append(Paragraph("What the Document Does Well", h2_style))
        for s in result["strengths"]:
            story.append(Paragraph(f"• {clean_text(s)}", bullet_style))
        story.append(Spacer(1, 4))

    # RULES CONSIDERED
    if result.get("rules_considered"):
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        story.append(Paragraph("Rules Considered", h2_style))
        for rule in result["rules_considered"]:
            story.append(Paragraph(f"• <b>{clean_text(rule.get('id',''))}</b>: {clean_text(rule.get('title',''))}", bullet_style))

    doc.build(story)
    return buffer.getvalue()
