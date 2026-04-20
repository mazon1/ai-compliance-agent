# Fire Extinguisher Compliance Checker

A focused AI-powered prototype that reviews a fire extinguisher procedure against a narrow set of OSHA-style requirements and produces an actionable compliance report for a non-technical safety manager.

## Why this scope
I intentionally scoped the solution to **portable fire extinguisher inspection and maintenance** because it is:
- clear and easy to validate
- well-suited to a focused compliance prototype
- practical to explain in a short assessment

## What it does
1. Accepts a safety procedure as pasted text or uploaded `.txt` / `.md`
2. Compares the procedure against a focused rule set:
   - monthly inspection
   - annual maintenance
   - accessibility / visibility
   - condition / damage
   - documentation / tags / records
3. Uses Claude to identify:
   - missing requirements
   - incorrect or weak practices
   - contradictions
   - vague wording where specifics are required
4. Produces a structured report with severity and recommended actions
5. Allows the report to be downloaded as a PDF

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

### 3) Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY="your_key_here"     # macOS / Linux
# or
set ANTHROPIC_API_KEY=your_key_here          # Windows CMD
# or use Streamlit secrets in deployment
```

### 4) Run locally
```bash
streamlit run app.py
```

## Streamlit deployment
Deploy on Streamlit Community Cloud and add:
- `ANTHROPIC_API_KEY` in app secrets

## Sample input documents
- `sample_docs/compliant.txt`
- `sample_docs/non_compliant.txt`

## Design decisions
- **Narrow scope over breadth**: one safety topic done well is more useful than a broad but shallow system
- **Hardcoded rule set**: faster, simpler, and more explainable for a time-boxed assessment
- **LLM for interpretation**: useful for spotting vague language, omissions, and contradictions in natural-language procedures
- **Friendly UI**: optimized for a safety manager rather than a developer

## Trade-offs
- I chose a focused rule set instead of full regulation retrieval to keep the prototype reliable and demoable.
- I avoided heavier orchestration frameworks because the workflow is straightforward: input → compare → report.

## Limitations
- The current prototype is limited to one safety topic.
- It uses a curated rule set rather than pulling regulations dynamically from the web.
- The quality of findings depends on the clarity of the input document and the LLM response.

## Error handling
- If Claude returns malformed JSON, the app falls back to a parsing-safe response with a warning.
- Empty input is blocked before analysis.
- The UI clearly warns if the API key is missing.

## What v2 would look like
- Expand to **Lockout/Tagout** using OSHA 29 CFR 1910.147
- Add retrieval from versioned regulation sources
- Support document chunking for longer procedures
- Add evidence highlighting directly in the uploaded document
- Add reviewer approval / sign-off workflow for human-in-the-loop use
