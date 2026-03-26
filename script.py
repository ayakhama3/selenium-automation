import os
import requests
import subprocess
import traceback
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===========================
# Connexion GSF
# ===========================
# ===========================
# Connexion GSF
# ===========================
def connexion_gsf(driver, wait, username, password):
    driver.get("https://gsf.ma/connexion")
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    print("✅ Connexion GSF effectuée")


# ===========================
# Connexion Marché Public
# ===========================
def connexion_marche_public(driver, wait, username, password):
    driver.get("https://www.marchespublics.gov.ma/index.php?page=agent.AgentHome")
    wait.until(EC.presence_of_element_located((By.ID, "ctl0_CONTENU_PAGE_identifiant"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.ID, "ctl0_CONTENU_PAGE_password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "ctl0_CONTENU_PAGE_authentificationButton"))).click()
    print("✅ Connexion Marché Public effectuée")


    # Cliquer sur "Accéder" si présent
    try:
        bouton_acces = wait.until(EC.element_to_be_clickable(
            (By.NAME, "ctl0$CONTENU_PAGE$repeaterListeServices$ctl0$ctl1")
        ))
        bouton_acces.click()
        print("✅ Bouton 'Accéder' cliqué automatiquement")
    except Exception as e:
        print("⚠️ Impossible de cliquer sur le bouton 'Accéder' :", e)


# ===========================
# Chercher une consultation
# ===========================
def chercher_consultation(driver, numero):
    try:
        element = driver.find_element(By.XPATH, f"//td[contains(text(), '{numero}')]")
        if element:
            element.click()
            print(f"✅ Consultation '{numero}' trouvée et ouverte")
            return True
    except (TimeoutException, NoSuchElementException):
        print(f"❌ Consultation '{numero}' non trouvée.")
        return False


# ===========================
# Navigation et téléchargement
# ===========================
def lancer_navigation(email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, lien_fichier, navigateur="chrome"):
    print("Début de la fonction lancer_navigation")
    driver = None
    try:
        # Choix du navigateur
        if navigateur.lower() == "chrome":
            print("Initialisation du driver Chrome")
            options = ChromeOptions()
            options.add_argument('--start-maximized')
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        elif navigateur.lower() == "edge":
            print("Initialisation du driver Edge")
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument('--start-maximized')
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError("Navigateur inconnu. Choisissez 'chrome' ou 'edge'.")

        print("Driver initialisé avec succès")

        wait = WebDriverWait(driver, 20)

        # Connexion aux plateformes
        print("Début de la connexion aux plateformes")
        connexion_marche_public(driver, wait, email_mp, mdp_mp)
        print("Connexion réussie")

        # Accès à "Toutes les consultations"
        try:
            toutes_consultations = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Toutes les consultations")))
            toutes_consultations.click()
            print("Lien 'Toutes les consultations' cliqué")
        except Exception as e:
            print(f"⚠️ Lien 'Toutes les consultations' introuvable ou timeout: {e}")
            return

        # Recherche du marché
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ref")))
        found = False
        for el in elements:
            if num_marche in el.text:
                print("✅ Consultation trouvée :", el.text)
                el.click()
                found = True
                break
        if not found:
            print(f"❌ Consultation '{num_marche}' non trouvée.")
            return

        # Extraire la référence
        html = driver.page_source
        split = html.split(num_marche)
        split2 = split[1].split("themes/images/picto-suivi.gif")
        split3 = split2[0].split("index.php?page=agent.DetailConsultation&amp;refConsultation=")
        refence = split3[1].split('">')[0]
        print(f"Référence extraite : {refence}")

        print(f"🔗 Redirection vers l'ouverture des plis : {refence}")
        driver.get(f"https://www.marchespublics.gov.ma/index.php?page=agent.ouvertureEtAnalyse&refConsultation={refence}")

        # Onglet secondaire
        of_elements = driver.find_elements(By.ID, "ctl0_CONTENU_PAGE_secondTab")
        if of_elements:
            of_elements[0].click()
        else:
            print("⚠️ Onglet secondaire introuvable")

        wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'tableau-ouverture')]")))

        # Création dossier
        if not os.path.exists(lien_fichier):
            os.makedirs(lien_fichier)

        # Télécharger les plis
        rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'tableau-ouverture')]//tbody/tr")
        for row in rows:
            try:
                num_pli = row.find_element(By.XPATH, "./td[2]").text.strip().replace(" ", "_")
                entreprise = row.find_element(By.XPATH, "./td[3]//span").text.strip().replace(" ", "_")
                lien_zip = row.find_element(By.XPATH, ".//a[contains(@href, 'DownloadPli')]").get_attribute("href")

                nom_fichier = f"{entreprise}_{num_pli}.zip"
                chemin_fichier = os.path.join(lien_fichier, nom_fichier)

                cookies = {c['name']: c['value'] for c in driver.get_cookies()}
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(lien_zip, cookies=cookies, headers=headers)

                if r.status_code == 200:
                    with open(chemin_fichier, "wb") as f:
                        f.write(r.content)
                    print(f"✅ Enregistré : {chemin_fichier}")
                else:
                    print(f"❌ Échec du téléchargement ({r.status_code})")
            except Exception as e:
                print("⚠️ Erreur lors du traitement d’un pli :", e)

        # Accès aux réponses
        try:
            bouton_reponse = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[alt='Acces aux reponses']")))
            bouton_reponse.click()
            print("✅ Accès aux réponses ouvert.")
        except Exception as e:
            print("⚠️ Impossible d’accéder aux réponses :", e)

        print("Fin de la fonction lancer_navigation")
        return True

    except Exception as e:
        print(f"Erreur dans lancer_navigation : {e}")
        raise
    finally:
        if driver:
            driver.quit()
            print("Driver fermé")
        print("📦 Téléchargement terminé, lancement du convertisseur...")
        subprocess.Popen([sys.executable, "convertisseur.py", lien_fichier])


# ===========================
# Variables de test
# ===========================
email_gsf = "finance.dpsale@gmail.com"
mdp_gsf = "1234"
email_mp = "PCAORACHIDIMH"
mdp_mp = "PCAORACHIDI*Q14*N"
num_marche = "MP2025XXXX"  # Remplacer par le numéro réel
lien_fichier = "./downloads"

# Lancer la navigation si exécution directe
if __name__ == "__main__":
    lancer_navigation(email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, lien_fichier, "chrome")
