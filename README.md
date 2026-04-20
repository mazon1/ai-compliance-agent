# Fire Extinguisher Compliance Checker

A focused AI-powered workflow that reviews a fire extinguisher procedure against a defined set of OSHA-style requirements and produces an actionable compliance report for a non-technical safety manager.

---

## Why this scope

I intentionally scoped the solution to **portable fire extinguisher inspection and maintenance** because it is:

- Clear and easy to validate  
- Well-suited to a focused compliance prototype  
- Practical to demonstrate end-to-end (input → analysis → report)  

This reflects a key principle in AI adoption: **start narrow, deliver value, then scale.**

---

## What it does

1. Accepts a safety procedure (paste or upload `.txt` / `.md`)
2. Compares the document against a focused compliance rule set:
   - Monthly inspection  
   - Annual maintenance  
   - Accessibility / visibility  
   - Condition / damage  
   - Documentation / tags / records  
3. Uses an LLM (Google Gemini) to:
   - Identify missing or incorrect requirements  
   - Flag vague or non-specific language  
   - Detect contradictions or weak practices  
4. Produces a structured, actionable compliance report:
   - Severity-based findings  
   - Clear recommendations  
   - Supporting evidence from the document  
5. Allows export as a PDF for operational use

---

## Project structure

```bash
.
├── app.py
├── analyzer.py
├── rules.py
├── utils.py
├── requirements.txt
├── README.md
├── sample_docs/
│   ├── compliant.txt
│   └── non_compliant.txt
└── outputs/
    └── sample_report.md
