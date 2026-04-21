# 🔥 Fire Extinguisher Compliance Checker

> Upload → Analyze → Get actionable compliance gaps in seconds

A focused AI-powered prototype that reviews a fire extinguisher procedure against a narrow set of OSHA-style requirements and produces an actionable compliance report for a non-technical safety manager.

Link to v1: Deployed on Streamlit: https://ai-compliance-agent.streamlit.app/
Link to v2: Deployed on Vercel: https://safety-sentinel-lime.vercel.app/

---

## Why this scope

I intentionally scoped the solution to **portable fire extinguisher inspection and maintenance** because it is:

- Clear and easy to validate  
- Well-suited to a focused compliance prototype  
- Practical to demonstrate in a short assessment  

---

## What it does

1. Accepts a safety procedure as pasted text or uploaded `.txt` / `.md`  
2. Compares the procedure against a focused rule set:
   - Monthly inspection  
   - Annual maintenance  
   - Accessibility / visibility  
   - Condition / damage  
   - Documentation / tags / records  
3. Uses an LLM (Google Gemini) to identify:
   - Missing requirements  
   - Incorrect or weak practices  
   - Contradictions  
   - Vague wording where specifics are required  
4. Produces a structured, actionable compliance report  
5. Allows the report to be downloaded as a PDF  

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
```

---

## Setup

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# or
.venv\Scripts\activate      # Windows
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Add your API key (Streamlit)

Create a `.streamlit/secrets.toml` file:

```toml
GOOGLE_API_KEY = "your_key_here"
```

### 4) Run locally

```bash
streamlit run app.py
```

---

## Streamlit deployment

Deploy on Streamlit Community Cloud and add:

```toml
GOOGLE_API_KEY = "your_key_here"
```

in **App Secrets**

---

## Sample input documents

- `sample_docs/compliant.txt`  
- `sample_docs/non_compliant.txt`  

---

## Design decisions

- Narrow scope over breadth → one safety topic done well  
- Hardcoded rule set → faster, more explainable, reliable for demo  
- LLM for interpretation → handles ambiguity, gaps, and vague language  
- Simple UI → designed for safety managers, not engineers  

---

## Trade-offs

- Focused rule set instead of full regulation retrieval  
- No heavy orchestration (kept workflow simple: input → compare → report)  

---

## Limitations

- Limited to one safety topic  
- Rules are static (not dynamically retrieved)  
- Output quality depends on document clarity and model response  

---

## Error handling

- JSON parsing fallback if model output is malformed  
- Clear UI validation for missing input  
- API key validation via Streamlit secrets  

---

## What v2 would look like

- Expand to **Lockout/Tagout (OSHA 29 CFR 1910.147)**  
- Add retrieval from live regulatory sources  
- Support long documents via chunking and accept PDF uploads
- Highlight issues directly inside the document  
- Add human-in-the-loop review workflow  

---

## Positioning 

This prototype demonstrates how AI can be embedded into **real safety workflows** to:

- Reduce manual compliance review time  
- Improve consistency of audits  
- Surface actionable gaps for non-technical users  
