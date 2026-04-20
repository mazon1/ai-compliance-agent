import json
import google.generativeai as genai
import streamlit as st
from rules import RULES

SYSTEM_PROMPT = """
You are an occupational safety compliance reviewer.
Your job is to compare a fire extinguisher procedure document against a narrow set of OSHA-style requirements.
Be practical, conservative, and actionable.
Do not invent laws beyond the provided rules.
Return JSON only.
"""

def build_prompt(document_text: str, strict_mode: bool) -> str:
    rules_text = "\n".join(
        [f"- {rule['id']}: {rule['title']} | {rule['requirement']}" for rule in RULES]
    )

    strictness = (
        "Be strict about vague language. If the document says things like 'regularly' or 'as needed' where a specific frequency is expected, flag it."
        if strict_mode else
        "Do not over-flag vague wording unless it affects compliance."
    )

    return f"""
{SYSTEM_PROMPT}

Review the following safety procedure for compliance against the provided rules.

RULES:
{rules_text}

DOCUMENT:
\"\"\"
{document_text}
\"\"\"

Instructions:
1. Determine whether the document appears compliant, partially compliant, or non-compliant for this narrow rule set.
2. Flag:
   - missing requirements
   - incorrect frequencies or values
   - outdated or weak practices
   - contradictions
   - vague language where specifics are needed
3. Provide evidence quotes from the document when possible.
4. Also identify strengths if the document clearly addresses a requirement.
5. Keep the output practical for a non-technical safety manager.

{strictness}

Return valid JSON in this exact shape:
{{
  "overall_status": "Compliant | Partially Compliant | Non-Compliant",
  "summary": "2-4 sentences",
  "issues": [
    {{
      "title": "short issue name",
      "severity": "High | Medium | Low",
      "why_it_matters": "1-2 sentences",
      "recommendation": "specific corrective action",
      "evidence": "quote or 'Not found'"
    }}
  ],
  "strengths": ["bullet 1", "bullet 2"],
  "rules_considered": [
    {{
      "id": "rule id",
      "title": "rule title"
    }}
  ]
}}
"""


def analyze_document(document_text: str, model_name: str, strict_mode: bool, source_name: str) -> dict:
    
    # 🔑 Configure Gemini
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = build_prompt(document_text, strict_mode)

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
    except Exception as e:
        return {
            "overall_status": "Partially Compliant",
            "summary": f"Model call failed: {str(e)}",
            "issues": [
                {
                    "title": "Model failure",
                    "severity": "High",
                    "why_it_matters": "The AI model did not return a response.",
                    "recommendation": "Check API key, model config, or retry.",
                    "evidence": str(e)
                }
            ],
            "strengths": [],
            "rules_considered": [{"id": r["id"], "title": r["title"]} for r in RULES],
            "document_name": source_name
        }

    # 🔍 JSON parsing (keep your strong logic)
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(raw_text[start:end+1])
        else:
            data = {
                "overall_status": "Partially Compliant",
                "summary": "The model response could not be parsed cleanly. Review raw output.",
                "issues": [
                    {
                        "title": "Parsing failure",
                        "severity": "Medium",
                        "why_it_matters": "The model output was not returned as valid JSON.",
                        "recommendation": "Retry analysis or tighten prompt constraints.",
                        "evidence": raw_text[:500]
                    }
                ],
                "strengths": [],
                "rules_considered": [{"id": r["id"], "title": r["title"]} for r in RULES]
            }

    # 📌 Add metadata
    data["document_name"] = source_name

    if "rules_considered" not in data or not data["rules_considered"]:
        data["rules_considered"] = [{"id": r["id"], "title": r["title"]} for r in RULES]

    return data
