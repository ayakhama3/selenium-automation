import os
import zipfile
import pdfplumber
import pandas as pd
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# === CONFIG ===
# Chemin vers Poppler (à adapter à ton installation)
POPPLER_PATH = r"C:\Users\HP\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# Chemin vers Tesseract (à adapter à ton installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === Dossiers ===
telechargements_dir = os.path.abspath("telechargements")
bureau = Path.home() / "Desktop"
dossier_excel = os.path.join(bureau, "fichiers_excel")

# Créer le dossier de sortie si nécessaire
os.makedirs(dossier_excel, exist_ok=True)

def extraire_zip(zip_path, dossier_destination):
    """Extrait le contenu d'un fichier ZIP dans un dossier spécifié."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dossier_destination)
            print(f"✅ Fichiers extraits de : {zip_path}")
    except zipfile.BadZipFile:
        print(f"❌ Erreur : Le fichier {zip_path} n'est pas un fichier ZIP valide.")
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction de {zip_path} : {e}")

def nettoyer_cellule(cell):
    """Nettoie le contenu d'une cellule en supprimant les sauts de ligne et espaces superflus."""
    if cell:
        return cell.replace("\n", " ").strip()
    return ""

def extraire_texte_image(pdf_path):
    """Extrait le texte d'un PDF scanné en utilisant OCR sur les images."""
    texte_complet = ""
    try:
        images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        for image in images:
            texte_complet += pytesseract.image_to_string(image, lang='fra') + "\n"
    except Exception as e:
        print(f"❌ Erreur OCR pour {pdf_path} : {e}")
    return texte_complet

def pdf_vers_excel(pdf_path, xlsx_path):
    """Convertit un fichier PDF en fichier Excel (tableaux ou OCR si nécessaire)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_tables = []
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        table_cleaned = [
                            [nettoyer_cellule(cell) for cell in row]
                            for row in table
                        ]
                        df = pd.DataFrame(table_cleaned[1:], columns=table_cleaned[0])

                        # 🔹 Renommer les colonnes dupliquées
                        df.columns = pd.io.parsers.ParserBase({'names': df.columns})._maybe_dedup_names(df.columns)

                        df.insert(0, "Page", page_num)
                        all_tables.append(df)

            if all_tables:
                result = pd.concat(all_tables, ignore_index=True)
            else:
                # Pas de tableau → utiliser OCR brut
                texte = extraire_texte_image(pdf_path)
                if texte.strip():
                    result = pd.DataFrame({"Texte OCR": texte.splitlines()})
                else:
                    result = pd.DataFrame({"Info": ["Aucune donnée extraite"]})

            result.to_excel(xlsx_path, index=False, engine='openpyxl')
            print(f"📄 Converti : {pdf_path} → {xlsx_path}")

    except Exception as e:
        print(f"❌ Erreur conversion {pdf_path} : {e}")

def pdf_vers_texte(pdf_path, txt_path):
    """Extrait le texte d'un PDF (OCR si nécessaire) et l'enregistre."""
    try:
        texte = extraire_texte_image(pdf_path)
        if texte:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(texte)
            print(f"📄 Texte extrait : {pdf_path} → {txt_path}")
        else:
            print(f"⚠️ Aucun texte extrait de : {pdf_path}")
    except Exception as e:
        print(f"❌ Erreur extraction texte {pdf_path} : {e}")

# === Traitement ZIP + PDF ===
for fichier in os.listdir(telechargements_dir):
    if fichier.endswith(".zip"):
        zip_path = os.path.join(telechargements_dir, fichier)
        nom_sans_ext = os.path.splitext(fichier)[0]
        dossier_temp = os.path.join(telechargements_dir, f"{nom_sans_ext}_extrait")
        os.makedirs(dossier_temp, exist_ok=True)

        extraire_zip(zip_path, dossier_temp)

        # Parcourir les PDF extraits
        for racine, _, fichiers in os.walk(dossier_temp):
            for nom_fichier in fichiers:
                if nom_fichier.endswith(".pdf"):
                    chemin_pdf = os.path.join(racine, nom_fichier)
                    nom_base = os.path.splitext(nom_fichier)[0]

                    chemin_xlsx = os.path.join(dossier_excel, f"{nom_base}.xlsx")
                    chemin_txt = os.path.join(dossier_excel, f"{nom_base}.txt")

                    pdf_vers_excel(chemin_pdf, chemin_xlsx)
                    pdf_vers_texte(chemin_pdf, chemin_txt)

print("✅ Tous les fichiers ont été traités.")








