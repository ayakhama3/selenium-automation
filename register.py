import tkinter as tk
from tkinter import messagebox
from db import ajouter_utilisateur

def run_register():
    fenetre = tk.Tk()
    fenetre.title("Créer un compte")
    fenetre.geometry("300x250")
    fenetre.configure(bg="white")

    tk.Label(fenetre, text="Créer un nouveau compte", bg="white", font=("Helvetica", 14, "bold")).pack(pady=20)

    tk.Label(fenetre, text="Nom d'utilisateur", bg="white").pack()
    entry_user = tk.Entry(fenetre)
    entry_user.pack(pady=5)

    tk.Label(fenetre, text="Mot de passe", bg="white").pack()
    entry_pass = tk.Entry(fenetre, show="*")
    entry_pass.pack(pady=5)

    def enregistrer():
        nom = entry_user.get()
        mdp = entry_pass.get()
        if nom == "" or mdp == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        if ajouter_utilisateur(nom, mdp):
            messagebox.showinfo("Succès", "Compte créé avec succès.")
            fenetre.destroy()
        else:
            messagebox.showerror("Erreur", "Nom d’utilisateur déjà utilisé.")

    tk.Button(fenetre, text="Créer le compte", command=enregistrer).pack(pady=15)

    fenetre.mainloop()


