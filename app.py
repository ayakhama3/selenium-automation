# app.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import threading
import os
import db
from register import run_register
from script import lancer_navigation  # script Selenium

# ---------------------- Interface 2 (Synchronisation) ----------------------
def launch_app_interface2():
    root = ctk.CTk()
    root.title("Synchronisation des Données")
    root.geometry("1100x700")
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("green")

    titre = ctk.CTkLabel(root, text="SYNCHRONISATION DES DONNÉES",
                         font=ctk.CTkFont(size=26, weight="bold"))
    titre.pack(pady=20)

    frame_principal = ctk.CTkFrame(root, corner_radius=15)
    frame_principal.pack(pady=10, padx=20, fill="both", expand=True)

    # --- Fonctions auxiliaires ---
    def creer_input(frame, texte, row, show=None):
        lbl = ctk.CTkLabel(frame, text=texte, font=ctk.CTkFont(size=14))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ctk.CTkEntry(frame, width=300, font=ctk.CTkFont(size=14), show=show)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def creer_frame_connexion(parent, titre_text):
        frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        label = ctk.CTkLabel(frame, text=titre_text,
                             font=ctk.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        return frame

    # --- FRAME GSF ---
    frame_gsf = creer_frame_connexion(frame_principal, "Connexion à GSF")
    frame_gsf.grid(row=0, column=0, padx=30, pady=20, sticky="n")

    img_gsf_path = os.path.join("images", "image.png")
    if os.path.exists(img_gsf_path):
        img_gsf = Image.open(img_gsf_path).resize((100, 100))
        photo_gsf = ctk.CTkImage(light_image=img_gsf, dark_image=img_gsf, size=(100, 100))
    else:
        photo_gsf = None
        print(f"⚠️ Image GSF introuvable : {img_gsf_path}")

    ctk.CTkLabel(frame_gsf, image=photo_gsf, text="").grid(row=1, column=0, columnspan=2, pady=10)
    entry_id_gsf = creer_input(frame_gsf, "Identifiant GSF :", row=2)
    entry_pwd_gsf = creer_input(frame_gsf, "Mot de passe :", row=3, show="*")

    # --- FRAME MARCHÉ PUBLIC ---
    frame_mp = creer_frame_connexion(frame_principal, "Connexion à Marché Public")
    frame_mp.grid(row=0, column=1, padx=30, pady=20, sticky="n")

    img_mp_path = os.path.join("images", "telechargement.jpeg")
    if os.path.exists(img_mp_path):
        img_mp = Image.open(img_mp_path).resize((100, 100))
        photo_mp = ctk.CTkImage(light_image=img_mp, dark_image=img_mp, size=(100, 100))
    else:
        photo_mp = None
        print(f"⚠️ Image MP introuvable : {img_mp_path}")

    ctk.CTkLabel(frame_mp, image=photo_mp, text="").grid(row=1, column=0, columnspan=2, pady=10)
    entry_id_mp = creer_input(frame_mp, "Identifiant MP :", row=2)
    entry_pwd_mp = creer_input(frame_mp, "Mot de passe :", row=3, show="*")
    entry_num_marche = creer_input(frame_mp, "Numéro du marché :", row=4)
    entry_lien = creer_input(frame_mp, "Dossier de téléchargement :", row=5)

    # Choisir dossier
    def choisir_dossier():
        dossier = filedialog.askdirectory(title="Choisir un dossier de téléchargement")
        if dossier:
            entry_lien.delete(0, "end")
            entry_lien.insert(0, dossier)

    ctk.CTkButton(frame_mp, text="📂 Choisir dossier...", command=choisir_dossier).grid(
        row=6, column=0, columnspan=2, pady=10
    )

    # Navigateur
    frame_nav = ctk.CTkFrame(root, corner_radius=10)
    frame_nav.pack(pady=10)
    lbl_nav = ctk.CTkLabel(frame_nav, text="Navigateur :", font=ctk.CTkFont(size=14))
    lbl_nav.pack(side="left", padx=10)
    var_nav = ctk.StringVar(value="chrome")
    ctk.CTkRadioButton(frame_nav, text="Chrome", variable=var_nav, value="chrome").pack(side="left", padx=10, pady=5)
    ctk.CTkRadioButton(frame_nav, text="Edge", variable=var_nav, value="edge").pack(side="left", padx=10, pady=5)

    # Barre de progression
    progress = ctk.CTkProgressBar(root, width=600)
    progress.set(0)
    progress.pack(pady=10)

    # Fonction synchronisation
    def lancer_sync():
        email_gsf = entry_id_gsf.get()
        mdp_gsf = entry_pwd_gsf.get()
        email_mp = entry_id_mp.get()
        mdp_mp = entry_pwd_mp.get()
        num_marche = entry_num_marche.get()
        dossier = entry_lien.get()
        navigateur = var_nav.get()

        if not dossier:
            messagebox.showwarning("Attention", "⚠️ Aucun dossier choisi !")
            return

        if messagebox.askyesno("Mémoriser", "Voulez-vous enregistrer vos informations pour la prochaine fois ?"):
            db.sauvegarder_parametres(email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier)

        def thread_function():
            try:
                trouve = lancer_navigation(email_gsf, mdp_gsf, email_mp, mdp_mp, num_marche, dossier, navigateur)
            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors de la synchronisation:\n{e}"))
                return

            root.after(0, lambda: progress.set(1))
            if not trouve:
                root.after(0, lambda: messagebox.showerror(
                    "Erreur", f"❌ Le numéro de consultation '{num_marche}' est introuvable."
                ))
            else:
                root.after(0, lambda: messagebox.showinfo("Terminé", "La synchronisation est terminée ✅"))

        threading.Thread(target=thread_function, daemon=True).start()

    # Bouton Lancer
    ctk.CTkButton(root, text="Lancer la synchronisation", command=lancer_sync).pack(pady=20)

    # Charger infos sauvegardées
    infos = db.charger_parametres()
    if infos:
        entry_id_gsf.insert(0, infos[0])
        entry_pwd_gsf.insert(0, infos[1])
        entry_id_mp.insert(0, infos[2])
        entry_pwd_mp.insert(0, infos[3])
        entry_num_marche.insert(0, infos[4])
        entry_lien.insert(0, infos[5])

    root.mainloop()


# ---------------- Interface 1 (Connexion) ----------------
def launch_app_interface1():
    root = ctk.CTk()
    root.title("Connexion à l'application")
    root.geometry("500x600")
    root.resizable(False, False)
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("green")

    # Icône
    icon_path = os.path.join("images", "icone.png")
    if os.path.exists(icon_path):
        icon_img = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_img)
        root.iconphoto(False, icon_photo)

    # Image de fond
    bg_path = os.path.join("images", "selenium.png")
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        window_width, window_height = 500, 600
        ratio = window_width / img.width
        new_height = int(img.height * ratio)
        img_resized = img.resize((window_width, new_height), Image.Resampling.LANCZOS)
        bg_ctkimage = ctk.CTkImage(light_image=img_resized, size=(window_width, new_height))
        bg_label = ctk.CTkLabel(root, image=bg_ctkimage, text="")
        bg_label.place(x=0, y=(window_height - new_height) // 2)

    # Frame login
    frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#ffffff", width=420, height=470)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Connexion", font=ctk.CTkFont(size=28, weight="bold"),
                 text_color="#0099ff").pack(pady=20)

    # Nom utilisateur
    ctk.CTkLabel(frame, text="Nom d'utilisateur", anchor="w",
                 font=ctk.CTkFont(size=14)).pack(pady=(10, 0), padx=30, fill="x")
    entry_user = ctk.CTkEntry(frame, width=350, corner_radius=10, border_width=1,
                              font=ctk.CTkFont(size=14))
    entry_user.pack(pady=5, padx=30, fill="x")

    # Mot de passe
    ctk.CTkLabel(frame, text="Mot de passe", anchor="w",
                 font=ctk.CTkFont(size=14)).pack(pady=(10, 0), padx=30, fill="x")
    entry_pass = ctk.CTkEntry(frame, width=350, corner_radius=10, border_width=1,
                              show="*", font=ctk.CTkFont(size=14))
    entry_pass.pack(pady=5, padx=30, fill="x")

    # Bouton voir/masquer
    def toggle_password():
        if entry_pass.cget("show") == "*":
            entry_pass.configure(show="")
        else:
            entry_pass.configure(show="*")

    ctk.CTkButton(frame, text="👁", width=40, height=35, command=toggle_password,
                  fg_color="#e0e0e0", hover_color="#c0c0c0").place(x=390, y=200)

    # Mot de passe oublié
    def mot_de_passe_oublie():
        messagebox.showinfo("Mot de passe oublié",
                            "Contactez l'administrateur pour réinitialiser votre mot de passe.")

    ctk.CTkButton(frame, text="Mot de passe oublié ?", command=mot_de_passe_oublie,
                  fg_color="transparent", text_color="#00bfff",
                  hover_color="#e6f7ff", font=ctk.CTkFont(size=12, weight="bold")
                  ).pack(pady=(5, 10))

    # Connexion
    def connexion_app():
        nom = entry_user.get()
        mdp = entry_pass.get()
        if db.verifier_utilisateur(nom, mdp):
            messagebox.showinfo("Connexion", f"Bienvenue {nom} ! ✅")
            root.destroy()
            launch_app_interface2()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect ❌")

    ctk.CTkButton(frame, text="Se connecter", command=connexion_app,
                  fg_color="#00bfff", hover_color="#33ccff",
                  font=ctk.CTkFont(size=16, weight="bold")
                  ).pack(pady=10, padx=40, fill="x")

    # Créer compte
    ctk.CTkButton(frame, text="Créer un compte", command=run_register,
                  fg_color="#ffffff", text_color="#00bfff",
                  hover_color="#e6f7ff", font=ctk.CTkFont(size=16, weight="bold")
                  ).pack(pady=10, padx=40, fill="x")

    root.mainloop()


# --- Lancement ---
if __name__ == "__main__":
    launch_app_interface1()

































































