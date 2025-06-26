# Gemini-Streamlit ATS Prototype

A lightweight resume-to-job-description matching tool built with **Google Gemini** and **Streamlit**.  
It lets you:

1. Convert each PDF resume page to an image and feed it to Gemini.
2. Compare the resume with any job description.
3. Return a percentage match and list missing keywords.
4. Generate a concise three-paragraph cover letter—all from one interface.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.9 + | Tested on 3.9 and 3.10 |
| Poppler      | Needed by `pdf2image` for PDF-to-JPEG conversion<br>• macOS: `brew install poppler`<br>• Ubuntu/Debian: `sudo apt-get install poppler-utils`<br>• Windows: download poppler binaries and add them to `PATH` |

---

## Quick Start

1. **Clone the repo**

   ```bash
   git clone https://github.com/peshalnepal/gemini-ats.git
   cd gemini-ats
2. **Create and activate a virtual environment**

   ```bash
    python -m venv venv
    # macOS / Linux
    source venv/bin/activate
    # Windows (PowerShell)
    venv\Scripts\Activate
3. **Install dependencies**

   ```bash
    pip install -r requirements.txt

4. **Add your Gemini API key**

    Create a file named .env in the project root:
   ```bash
    GEMINI_API_KEY="your_secret_api_key"

5. **Run the app**

   ```bash
    streamlit run app.py

Streamlit will print a local URL (usually http://localhost:8501).
Open it in your browser to test the application.

