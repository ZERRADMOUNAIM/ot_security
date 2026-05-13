# OTMindset

**Intelligent OT Compliance & Thinking Mapper**

AI-powered platform that analyzes Operational Technology (OT) cybersecurity requests and produces intelligent compliance assessments mapped to OTCC controls and IEC 62443 references.

---

## Features

- 🧠 **AI-Powered Analysis** — Uses Groq API (LLaMA 3.3 70B) for deep OT-aware reasoning
- 🛡️ **8-Card Assessment** — Operational context, risks, controls, OTCC & IEC 62443 mappings, decision guidance
- 📊 **Risk Scoring** — Automated risk score calculation with severity badges
- 📋 **Analysis History** — Full history with search and pagination
-   **Security Hardened** — CSRF protection, rate limiting, input validation, prompt injection defense
- 🎨 **SOC Dashboard UI** — Dark cybersecurity theme with glassmorphism and gradient accents

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| AI Engine | Groq API — LLaMA 3.3 70B Versatile |
| Frontend | TailwindCSS + Alpine.js |
| Database | SQLite + SQLAlchemy |
| Auth | Flask-Login |

---

## Installation

### 1. Clone & Setup Virtual Environment

```bash
cd ot_security
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your-groq-api-key-here
SECRET_KEY=your-secret-key-change-this
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the Application

```bash
python run.py
```

Visit: **http://localhost:5000**

---

## API Usage

### Analyze an OT Scenario

```
POST /api/analyze
Content-Type: application/json

{
  "scenario": "Vendor requires remote access to SCADA historian"
}
```

### Response Structure

```json
{
  "id": 1,
  "scenario": "...",
  "result": {
    "operational_context": "...",
    "missing_information": [],
    "security_questions": [],
    "potential_risks": [],
    "recommended_controls": [],
    "otcc_controls": [],
    "iec62443_references": [],
    "decision_guidance": {
      "decision": "Proceed with Controls",
      "severity": "High",
      "reason": "..."
    }
  },
  "risk_score": 65,
  "severity": "High"
}
```

---

## Project Architecture

```
ot_security/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # Flask blueprints
│   ├── services/            # AI engine & mappers
│   ├── templates/           # Jinja2 templates
│   ├── static/              # CSS & JS
│   └── utils/               # Validators & helpers
├── config.py                # Configuration
├── run.py                   # Entry point
├── requirements.txt
└── .env
```

---

## License

MIT
