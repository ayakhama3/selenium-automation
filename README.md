# 🤖 Selenium Automation — Public Tender Retrieval & Document Conversion

🇬🇧 English | [🇫🇷 Français](README.fr.md)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-automation-43B02A?logo=selenium&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6feb)
![SQLite](https://img.shields.io/badge/SQLite-local%20storage-003B57?logo=sqlite&logoColor=white)

A Windows desktop tool that automates a repetitive back-office workflow: it signs in to two web portals (**GSF** and the Moroccan public procurement portal **marchespublics.gov.ma**), finds a tender by its number, opens the bids, downloads the submitted files, then converts the downloaded PDFs into spreadsheets and text files using OCR.

## ✨ Features

- **Desktop interface** (CustomTkinter): local account creation / login, browser choice (Chrome or Edge) and download folder selection.
- **Browser automation** (Selenium + `webdriver-manager`): sign-in to both portals, tender lookup by number, opening each bid and downloading its documents.
- **Document conversion**: ZIP extraction, table extraction from PDFs to Excel (`pdfplumber` + `pandas`), and **OCR fallback** for scanned pages (`pytesseract` + Poppler).
- **Local persistence** (SQLite): user accounts (SHA-256 hashed passwords) and saved synchronization settings.

## 🧱 Architecture

```
app.py            Desktop GUI (login, settings, "Start synchronization")
 ├─ register.py   Account creation window
 ├─ db.py         SQLite storage (users, saved settings)
 └─ script.py     Selenium workflow: login → find tender → download bids
      └─ convertisseur.py   ZIP → PDF → Excel / text (with OCR fallback)
```

## 🚀 Getting started

### Prerequisites

- Python 3.10+
- Google Chrome or Microsoft Edge
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://github.com/oschwartz10612/poppler-windows) (only needed for the OCR / PDF conversion step)

### Installation

```bash
git clone https://github.com/ayakhama3/selenium-automation.git
cd selenium-automation

python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your own values (only needed to run `script.py` directly). If Tesseract or Poppler are not on your `PATH`, set `TESSERACT_CMD` and `POPPLER_PATH`.

### Run

```bash
python app.py
```

## 🔒 Security notes

- Credentials are **never** stored in the source code. Use environment variables (`.env`, git-ignored) or the in-app settings.
- Saved portal settings live in a local SQLite file (`utilisateurs.db`, git-ignored). They are stored locally on your machine only; encrypting them (e.g. via the OS keyring) is a planned improvement.
- Use this tool only with accounts you are authorized to use and in compliance with the portals' terms of service.

## ⚠️ Known limitations

- Selenium selectors depend on the portals' current HTML; a redesign of either site may require updates.
- Windows-oriented defaults (Tesseract install path), though paths are configurable.

## 🔭 Roadmap

- Encrypt saved settings (OS keyring)
- Unit tests for the conversion module
- Headless mode and scheduled runs

## 👩‍💻 Author

**Aya Khama** — Data Science & AI engineering student (EMSI)
[LinkedIn](https://www.linkedin.com/in/aya-khama-160752387/) · [GitHub](https://github.com/ayakhama3)
