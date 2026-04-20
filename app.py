import os
import streamlit as st
from analyzer import analyze_document
from utils import generate_pdf_bytes

st.set_page_config(
    page_title="Fire Extinguisher Compliance Checker",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Fire Extinguisher Compliance Checker")
st.caption("AI-powered review of safety procedures against OSHA portable fire extinguisher requirements.")

with st.expander("What this prototype checks", expanded=False):
    st.markdown(
        """
        This prototype evaluates a safety procedure against a focused subset of OSHA-inspired
        portable fire extinguisher requirements, including:
        - Monthly inspection
        - Annual maintenance
        - Accessibility / visibility
        - Condition / damage
        - Documentation / tags / records
        """
    )

left, right = st.columns([1.2, 1])

with left:
    st.subheader("1) Provide a safety procedure")
    upload = st.file_uploader("Upload a .txt or .md file", type=["txt", "md"])
    pasted = st.text_area(
        "Or paste the procedure text",
        height=320,
        placeholder="Paste a fire extinguisher inspection or maintenance procedure here..."
    )

with right:
    st.subheader("2) Settings")
    model_name = st.selectbox(
        "Claude model",
        options=["claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"],
        index=0
    )
    strict_mode = st.checkbox("Flag vague language aggressively", value=True)
    st.info(
        "Tip: keep the scope narrow. This prototype is designed for portable fire extinguisher procedures."
    )

doc_text = ""
source_name = "pasted_text"

if upload is not None:
    doc_text = upload.read().decode("utf-8", errors="ignore")
    source_name = upload.name
elif pasted.strip():
    doc_text = pasted.strip()

analyze = st.button("Analyze Compliance", type="primary", use_container_width=True)

if analyze:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("Missing ANTHROPIC_API_KEY. Set it in your environment or Streamlit secrets before running.")
        st.stop()

    if not doc_text.strip():
        st.warning("Please upload or paste a procedure before analyzing.")
        st.stop()

    with st.spinner("Reviewing document against OSHA-style requirements..."):
        try:
            result = analyze_document(
                document_text=doc_text,
                api_key=api_key,
                model_name=model_name,
                strict_mode=strict_mode,
                source_name=source_name
            )
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.success("Analysis complete.")
    st.subheader("3) Compliance Report")

    st.markdown(f"**Document:** {result['document_name']}")
    st.markdown(f"**Overall status:** {result['overall_status']}")
    st.markdown(f"**Summary:** {result['summary']}")

    if result["issues"]:
        st.markdown("### Findings")
        for idx, issue in enumerate(result["issues"], start=1):
            severity = issue.get("severity", "Medium")
            if severity.lower() == "high":
                st.error(
                    f"**{idx}. {issue.get('title','Issue')}**  \n"
                    f"**Severity:** {severity}  \n"
                    f"**Why it matters:** {issue.get('why_it_matters','')}  \n"
                    f"**Recommendation:** {issue.get('recommendation','')}  \n"
                    f"**Evidence from document:** {issue.get('evidence','Not found')}"
                )
            elif severity.lower() == "medium":
                st.warning(
                    f"**{idx}. {issue.get('title','Issue')}**  \n"
                    f"**Severity:** {severity}  \n"
                    f"**Why it matters:** {issue.get('why_it_matters','')}  \n"
                    f"**Recommendation:** {issue.get('recommendation','')}  \n"
                    f"**Evidence from document:** {issue.get('evidence','Not found')}"
                )
            else:
                st.info(
                    f"**{idx}. {issue.get('title','Issue')}**  \n"
                    f"**Severity:** {severity}  \n"
                    f"**Why it matters:** {issue.get('why_it_matters','')}  \n"
                    f"**Recommendation:** {issue.get('recommendation','')}  \n"
                    f"**Evidence from document:** {issue.get('evidence','Not found')}"
                )
    else:
        st.success("No major issues were flagged for the scoped rule set.")

    if result.get("strengths"):
        st.markdown("### What the document does well")
        for item in result["strengths"]:
            st.markdown(f"- {item}")

    if result.get("rules_considered"):
        with st.expander("Rules considered", expanded=False):
            for rule in result["rules_considered"]:
                st.markdown(f"- **{rule['id']}**: {rule['title']}")

    st.markdown("### Download report")
    pdf_bytes = generate_pdf_bytes(result)
    st.download_button(
        "Download PDF report",
        data=pdf_bytes,
        file_name="compliance_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    with st.expander("Raw JSON output", expanded=False):
        st.json(result)
