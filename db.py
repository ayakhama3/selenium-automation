import sqlite3
import hashlib

# =========================
# TABLE UTILISATEURS
# =========================
def creer_table_utilisateurs():
    conn = sqlite3.connect("utilisateurs.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hacher_mot_de_passe(mdp):
    """Hashage SHA-256 du mot de passe"""
    return hashlib.sha256(mdp.encode()).hexdigest()

def ajouter_utilisateur(nom, mot_de_passe):
    """Ajoute un utilisateur avec mot de passe haché"""
    try:
        conn = sqlite3.connect("utilisateurs.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (nom, mot_de_passe) VALUES (?, ?)",
                    (nom, hacher_mot_de_passe(mot_de_passe)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # utilisateur déjà existant
    finally:
        conn.close()

def verifier_utilisateur(nom, mot_de_passe):
    """Vérifie si un utilisateur existe"""
    conn = sqlite3.connect("utilisateurs.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilisateurs WHERE nom = ? AND mot_de_passe = ?",
                (nom, hacher_mot_de_passe(mot_de_passe)))
    utilisateur = cur.fetchone()
    conn.close()
    return utilisateur is not None

# =========================
# TABLE PARAMETRES SYNC
# =========================
def creer_table_parametres():
    conn = sqlite3.connect("utilisateurs.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parametres_sync (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_gsf TEXT,
            mdp_gsf TEXT,
            email_mp TEXT,
            mdp_mp TEXT,
            num_marche TEXT,
            dossier TEXT
        )
    """)
    conn.commit()
    conn.close()

def sauvegarder_parametres(email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier):
    conn = sqlite3.connect("utilisateurs.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM parametres_sync")
    cur.execute("""
        INSERT INTO parametres_sync (email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier))
    conn.commit()
    conn.close()

def charger_parametres():
    conn = sqlite3.connect("utilisateurs.db")
    cur = conn.cursor()
    cur.execute("SELECT email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier FROM parametres_sync LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row if row else None

# =========================
# INIT AUTO
# =========================
creer_table_utilisateurs()
creer_table_parametres()




