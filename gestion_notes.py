import json
import tkinter as tk
from tkinter import messagebox

# Dictionnaire global pour stocker les données des étudiants
etudiants = {}

# Charger les données des étudiants à partir d’un fichier JSON
def charger_donnees():
    global etudiants
    try:
        with open("etudiants.json", "r") as fichier:
            etudiants.update(json.load(fichier))
    except FileNotFoundError:
        pass

# Enregistrer les données des étudiants dans un fichier JSON
def sauvegarder_donnees():
    with open("etudiants.json", "w") as fichier:
        json.dump(etudiants, fichier, indent=4)

# Ajouter un étudiant ou mettre à jour sa note dans une matière
def ajouter_etudiant_interface(nom, matiere, note):
    global etudiants
    if not nom or not matiere or not note:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    
    try:
        note = float(note)
        if not (0 <= note <= 20):
            messagebox.showerror("Erreur", "La note doit être entre 0 et 20.")
            return
    except ValueError:
        messagebox.showerror("Erreur", "La note doit être un nombre.")
        return
    
    # Ajouter ou mettre à jour la note de l’étudiant
    if nom not in etudiants:
        etudiants[nom] = {}
    etudiants[nom][matiere] = note
    messagebox.showinfo("Succès", f"Les données pour '{nom}' ont été ajoutées ou mises à jour.")
    sauvegarder_donnees()

# Supprimer un étudiant du dictionnaire
def supprimer_etudiant(nom):
    global etudiants
    if nom in etudiants:
        del etudiants[nom]
        sauvegarder_donnees()
        messagebox.showinfo("Succès", f"L'étudiant '{nom}' a été supprimé.")
    else:
        messagebox.showerror("Erreur", f"L'étudiant '{nom}' n'existe pas.")

# Afficher les moyennes de chaque étudiant dans une nouvelle fenêtre
def afficher_moyennes():
    fenetre_moyennes = tk.Toplevel()
    fenetre_moyennes.title("Moyennes des étudiants")

    total_notes = 0
    total_matieres = 0
    lignes = []
    
    # Calcul des moyennes individuelles et cumul des notes
    for nom, matieres in etudiants.items():
        moy_etudiant = sum(matieres.values()) / len(matieres)
        lignes.append((nom, moy_etudiant))
        total_notes += sum(matieres.values())
        total_matieres += len(matieres)

    # Trier les étudiants par moyenne décroissante
    lignes.sort(key=lambda x: x[1], reverse=True)

    # Afficher les résultats triés
    for nom, moyenne in lignes:
        tk.Label(fenetre_moyennes, text=f"{nom}: {moyenne:.2f}").pack()

    # Afficher la moyenne générale de la classe
    if total_matieres > 0:
        moy_classe = total_notes / total_matieres
        tk.Label(fenetre_moyennes, text=f"\nMoyenne générale de la classe : {moy_classe:.2f}").pack()
    else:
        tk.Label(fenetre_moyennes, text="Aucune donnée disponible.").pack()

# Rechercher un étudiant et afficher ses notes dans une fenêtre
def rechercher_etudiant_interface(nom):
    if nom in etudiants:
        notes = etudiants[nom]
        resultats = "\n".join([f"{matiere}: {note}" for matiere, note in notes.items()])
        messagebox.showinfo("Résultat de la recherche", f"Notes pour {nom} :\n{resultats}")
    else:
        messagebox.showerror("Erreur", f"L'étudiant '{nom}' n'existe pas.")

# Créer l'interface graphique principale
def interface_principale():
    charger_donnees()
    fenetre = tk.Tk()
    fenetre.title("Gestion des notes des étudiants")

    # Formulaire pour ajouter une note
    tk.Label(fenetre, text="Nom de l'étudiant").grid(row=0, column=0, pady=5)
    entry_nom = tk.Entry(fenetre)
    entry_nom.grid(row=0, column=1, pady=5)

    tk.Label(fenetre, text="Matière").grid(row=1, column=0, pady=5)
    entry_matiere = tk.Entry(fenetre)
    entry_matiere.grid(row=1, column=1, pady=5)

    tk.Label(fenetre, text="Note").grid(row=2, column=0, pady=5)
    entry_note = tk.Entry(fenetre)
    entry_note.grid(row=2, column=1, pady=5)

    btn_ajouter = tk.Button(
        fenetre, text="Ajouter/Mise à jour",
        command=lambda: ajouter_etudiant_interface(entry_nom.get(), entry_matiere.get(), entry_note.get())
    )
    btn_ajouter.grid(row=3, column=0, columnspan=2, pady=10)

    # Bouton pour afficher les moyennes
    btn_moyennes = tk.Button(fenetre, text="Afficher les moyennes", command=afficher_moyennes)
    btn_moyennes.grid(row=4, column=0, columnspan=2, pady=10)

    # Zone pour rechercher un étudiant
    tk.Label(fenetre, text="Nom de l'étudiant à rechercher").grid(row=5, column=0, pady=5)
    entry_recherche = tk.Entry(fenetre)
    entry_recherche.grid(row=5, column=1, pady=5)

    btn_rechercher = tk.Button(
        fenetre, text="Rechercher",
        command=lambda: rechercher_etudiant_interface(entry_recherche.get())
    )
    btn_rechercher.grid(row=6, column=0, columnspan=2, pady=10)

    # Zone pour supprimer un étudiant
    tk.Label(fenetre, text="Nom de l'étudiant à supprimer").grid(row=7, column=0, pady=5)
    entry_suppression = tk.Entry(fenetre)
    entry_suppression.grid(row=7, column=1, pady=5)

    btn_supprimer = tk.Button(
        fenetre, text="Supprimer",
        command=lambda: supprimer_etudiant(entry_suppression.get())
    )
    btn_supprimer.grid(row=8, column=0, columnspan=2, pady=10)

    # lancer l'interface
    fenetre.mainloop()

# Lancer l'application
if __name__ == "__main__":
    interface_principale()
