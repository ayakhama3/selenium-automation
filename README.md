# 🤖 Automatisation de la synchronisation des marchés publics

Application de bureau réalisée en binôme lors d'un stage à la **Direction Provinciale de l'Éducation Nationale de Salé (DPEN Salé), département Finance**. Elle synchronise les dossiers de marchés publics entre **marchespublics.gov.ma** et **gsf.ma**.

## 🎯 Problème
Récupérer à la main les pièces de chaque marché, les archiver, les convertir puis les déposer sur un second portail : tâche répétitive, longue et source d'erreurs.

## 🔄 Workflow
```
Lancement de l'application
   ↓ Authentification simultanée (marchespublics.gov.ma + gsf.ma)
   ↓ Recherche automatique des marchés ciblés
   ↓ Téléchargement des PDF officiels
   ↓ Regroupement dans une archive ZIP
   ↓ Conversion PDF → Excel
   ↓ Envoi des fichiers Excel via l'API sécurisée de gsf.ma
   ↓ Confirmation de succès
```

## 🔑 Fonctionnalités
- Interface graphique **CustomTkinter** avec inscription / connexion des agents (base SQLite, mots de passe hachés)
- Navigation automatisée **Selenium** (Chrome / Edge)
- Extraction des tableaux des PDF (**pdfplumber**) avec repli OCR (**pytesseract**)
- Transmission automatique via API (**requests**)
- Packagé en exécutable **.exe** pour un déploiement direct auprès des agents

## 📁 Structure
| Fichier | Rôle |
|---|---|
| `app.py` | Interface graphique et orchestration |
| `register.py`, `db.py` | Inscription, authentification des utilisateurs (SQLite) |
| `script.py` | Automatisation Selenium : connexion, recherche, téléchargement, envoi |
| `convertisseur.py` | Décompression des ZIP et conversion PDF → Excel |

## 🛠️ Stack
Python · Selenium · CustomTkinter · pandas · pdfplumber · pytesseract · requests · SQLite · PyInstaller

## 🚀 Lancement
```bash
pip install -r requirements.txt
python app.py
```
> 🔒 Aucun identifiant ni document officiel n'est publié dans ce dépôt.

## 👥 Auteurs
Aya Khama et son binôme · stage DPEN Salé · [LinkedIn](https://www.linkedin.com/in/aya-khama-160752387)
