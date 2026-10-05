import streamlit as st
from pathlib import Path
import json
import re
from datetime import datetime

st.set_page_config(page_title="AI Document Checklist Generator", page_icon="📋", layout="wide")

st.title("📋 AI Document Checklist Generator")
st.write("Upload a document and generate a structured checklist from its contents.")

# Optional imports: the app still starts if a heavy AI package has an environment issue.
try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

try:
    import pandas as pd
except Exception:
    pd = None

def extract_text(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()

    if suffix == ".pdf":
        if PdfReader is None:
            return "", "pypdf is not available."
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text, ""

    if suffix == ".docx":
        if Document is None:
            return "", "python-docx is not available."
        doc = Document(uploaded_file)
        text = "\n".join(p.text for p in doc.paragraphs)
        for table in doc.tables:
            for row in table.rows:
                text += "\n" + " | ".join(cell.text for cell in row.cells)
        return text, ""

    if suffix in [".txt", ".md"]:
        return data.decode("utf-8", errors="ignore"), ""

    if suffix in [".csv", ".xlsx", ".xls"]:
        if pd is None:
            return "", "pandas is not available."
        if suffix == ".csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df.to_string(index=False), ""

    return "", "Supported files: PDF, DOCX, TXT, MD, CSV, XLSX."

def generate_checklist(text):
    """Rule-based baseline checklist. It is intentionally reliable offline.
    You can connect Gemini/other LLM logic later in ai_engine.py.
    """
    text_low = text.lower()
    checklist = []

    rules = [
        ("Identity / Applicant Details", ["name", "applicant", "student", "employee", "candidate", "id"]),
        ("Address Proof", ["address", "residence", "residential", "utility bill"]),
        ("Government ID", ["aadhaar", "aadhar", "passport", "pan card", "voter", "driving licence", "driving license"]),
        ("Photograph", ["photo", "photograph", "passport size"]),
        ("Educational Documents", ["education", "degree", "marksheet", "mark sheet", "certificate", "qualification"]),
        ("Employment Documents", ["employment", "experience", "salary", "joining", "relieving", "offer letter"]),
        ("Financial Documents", ["bank", "income", "salary slip", "income tax", "itr", "financial"]),
        ("Signature", ["signature", "signed", "sign"]),
        ("Application / Form", ["application form", "form", "application"]),
        ("Supporting Documents", ["supporting document", "attachment", "enclosure"]),
    ]

    for title, keywords in rules:
        matches = [k for k in keywords if k in text_low]
        if matches:
            checklist.append({
                "Document / Requirement": title,
                "Detected": "Yes",
                "Keywords": ", ".join(matches),
                "Status": "☐ Pending"
            })

    if not checklist:
        checklist = [{
            "Document / Requirement": "Review source document manually",
            "Detected": "No specific document requirement detected",
            "Keywords": "",
            "Status": "☐ Pending"
        }]

    return checklist

def make_markdown(checklist, source_name):
    lines = [
        "# AI Document Checklist",
        "",
        f"**Source:** {source_name}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| # | Document / Requirement | Detected | Status |",
        "|---:|---|---|---|"
    ]
    for i, item in enumerate(checklist, 1):
        lines.append(
            f"| {i} | {item['Document / Requirement']} | "
            f"{item['Detected']} | {item['Status']} |"
        )
    return "\n".join(lines)

uploaded = st.file_uploader(
    "Upload your document",
    type=["pdf", "docx", "txt", "md", "csv", "xlsx"],
)

if uploaded:
    text, error = extract_text(uploaded)
    if error:
        st.error(error)
    else:
        st.success(f"Extracted {len(text):,} characters from {uploaded.name}.")
        with st.expander("Preview extracted text"):
            st.text(text[:6000] if text else "No text extracted.")

        if st.button("✨ Generate Checklist", type="primary"):
            checklist = generate_checklist(text)

            st.subheader("Generated Checklist")
            if pd:
                st.dataframe(pd.DataFrame(checklist), use_container_width=True, hide_index=True)
            else:
                for i, item in enumerate(checklist, 1):
                    st.write(f"{i}. {item['Document / Requirement']} — {item['Status']}")

            md = make_markdown(checklist, uploaded.name)
            st.download_button(
                "⬇️ Download Checklist (Markdown)",
                data=md,
                file_name="document_checklist.md",
                mime="text/markdown"
            )

            st.download_button(
                "⬇️ Download Checklist (JSON)",
                data=json.dumps(checklist, indent=2),
                file_name="document_checklist.json",
                mime="application/json"
            )
else:
    st.info("Upload a document to begin.")
    st.markdown("""
### Project features
- PDF/DOCX/TXT/CSV/XLSX document input
- Text extraction
- Automatic document/requirement detection
- Interactive checklist
- Markdown and JSON export
- Offline baseline logic, so the application can run without an API key
""")
