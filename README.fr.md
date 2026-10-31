# 🤖 Selenium Automation — Récupération d'appels d'offres & conversion de documents

[🇬🇧 English](README.md) | 🇫🇷 Français

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-automatisation-43B02A?logo=selenium&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6feb)
![SQLite](https://img.shields.io/badge/SQLite-stockage%20local-003B57?logo=sqlite&logoColor=white)

Outil de bureau (Windows) qui automatise une tâche administrative répétitive : il se connecte à deux portails web (**GSF** et le portail marocain des marchés publics **marchespublics.gov.ma**), retrouve une consultation à partir de son numéro, ouvre les plis, télécharge les fichiers déposés, puis convertit les PDF téléchargés en tableurs et fichiers texte grâce à l'OCR.

## ✨ Fonctionnalités

- **Interface de bureau** (CustomTkinter) : création de compte / connexion locale, choix du navigateur (Chrome ou Edge) et du dossier de téléchargement.
- **Automatisation du navigateur** (Selenium + `webdriver-manager`) : connexion aux deux portails, recherche de la consultation par numéro, ouverture de chaque pli et téléchargement de ses documents.
- **Conversion de documents** : extraction des ZIP, extraction des tableaux des PDF vers Excel (`pdfplumber` + `pandas`) et **OCR de secours** pour les pages scannées (`pytesseract` + Poppler).
- **Persistance locale** (SQLite) : comptes utilisateurs (mots de passe hachés en SHA-256) et paramètres de synchronisation enregistrés.

## 🧱 Architecture

```
app.py            Interface (connexion, paramètres, « Lancer la synchronisation »)
 ├─ register.py   Fenêtre de création de compte
 ├─ db.py         Stockage SQLite (utilisateurs, paramètres)
 └─ script.py     Scénario Selenium : connexion → recherche → téléchargement des plis
      └─ convertisseur.py   ZIP → PDF → Excel / texte (avec OCR de secours)
```

## 🚀 Démarrage

### Prérequis

- Python 3.10+
- Google Chrome ou Microsoft Edge
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) et [Poppler](https://github.com/oschwartz10612/poppler-windows) (uniquement pour l'étape OCR / conversion PDF)

### Installation

```bash
git clone https://github.com/ayakhama3/selenium-automation.git
cd selenium-automation

python -m venv venv
venv\Scripts\activate          # Linux/macOS : source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copiez `.env.example` vers `.env` et renseignez vos propres valeurs (nécessaire seulement pour lancer `script.py` directement). Si Tesseract ou Poppler ne sont pas dans le `PATH`, définissez `TESSERACT_CMD` et `POPPLER_PATH`.

### Lancement

```bash
python app.py
```

## 🔒 Sécurité

- Les identifiants ne sont **jamais** écrits dans le code source. Utilisez des variables d'environnement (`.env`, ignoré par Git) ou les paramètres de l'application.
- Les paramètres des portails sont enregistrés dans un fichier SQLite local (`utilisateurs.db`, ignoré par Git), uniquement sur votre machine ; leur chiffrement (par exemple via le trousseau du système) est une amélioration prévue.
- N'utilisez cet outil qu'avec des comptes dont vous avez l'autorisation, dans le respect des conditions d'utilisation des portails.

## ⚠️ Limites connues

- Les sélecteurs Selenium dépendent du HTML actuel des portails : une refonte d'un des sites peut nécessiter des ajustements.
- Valeurs par défaut orientées Windows (chemin de Tesseract), bien que les chemins soient configurables.

## 🔭 Pistes d'amélioration

- Chiffrer les paramètres enregistrés (trousseau du système)
- Tests unitaires du module de conversion
- Mode sans interface (headless) et exécutions planifiées

## 👩‍💻 Auteure

**Aya Khama** — Étudiante ingénieure Data Science & IA (EMSI)
[LinkedIn](https://www.linkedin.com/in/aya-khama-160752387/) · [GitHub](https://github.com/ayakhama3)
