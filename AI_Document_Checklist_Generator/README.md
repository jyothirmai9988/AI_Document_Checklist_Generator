# AI Document Checklist Generator

A beginner-friendly Streamlit project that reads common document formats and
generates a structured checklist.

## Python version

Python 3.11.9

## Included features

- PDF text extraction with pypdf
- DOCX text extraction with python-docx
- TXT/Markdown support
- CSV/XLSX support
- Automatic requirement detection
- Checklist display in Streamlit
- JSON and Markdown downloads
- Optional AI extension point

## Project structure

```text
AI_Document_Checklist_Generator/
├── app.py
├── ai_engine.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
└── outputs/
```

## Windows setup

Open the project folder in VS Code.

### 1. Create virtual environment

```powershell
py -3.11 -m venv .venv
```

### 2. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install packages

If `pip` is not recognized, use Python to invoke pip:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run Streamlit

```powershell
python -m streamlit run app.py
```

The browser should open the Streamlit application.

## Tesseract OCR

`pytesseract` is only the Python wrapper. The Tesseract OCR engine itself
must be installed separately if you want OCR for scanned/image-only PDFs.

After installing Tesseract, make sure its executable is available in PATH.
Typical Windows installation location:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Troubleshooting

### 'pip' is not recognized

Do not use:

```powershell
pip install ...
```

Use:

```powershell
python -m pip install ...
```

### Streamlit is not recognized

Use:

```powershell
python -m streamlit run app.py
```

### Check Python version

```powershell
python --version
```

Expected:

```text
Python 3.11.9
```

### Check Streamlit installation

```powershell
python -m streamlit --version
```

## Note

The included checklist engine is an offline baseline. It does not require
an API key. `ai_engine.py` provides a clean extension point for Gemini/LLM
integration after the basic project is running.
