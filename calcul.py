import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import threading

class CalculApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calcul App")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        self.current_question = 0
        self.score = 0
        self.time_remaining = 30  # Temps en secondes
        self.difficulty_level = tk.StringVar()

        self.label_difficulty = tk.Label(master, text="Niveau de difficulté :", font=("Helvetica", 12), bg="#f0f0f0")
        self.label_difficulty.pack(pady=(20, 5))
        self.combobox_difficulty = ttk.Combobox(master, values=["Facile", "Moyen", "Difficile"], state="readonly", textvariable=self.difficulty_level)
        self.combobox_difficulty.current(0)
        self.combobox_difficulty.pack(pady=5)

        self.button_start = tk.Button(master, text="Démarrer", command=self.start_game, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief=tk.FLAT)
        self.button_start.pack(pady=10, ipady=5, ipadx=10)

    def start_game(self):
        difficulty = self.difficulty_level.get()
        if difficulty:
            self.label_difficulty.destroy()
            self.combobox_difficulty.destroy()
            self.button_start.destroy()

            self.label_question = tk.Label(self.master, text="", font=("Helvetica", 16), bg="#f0f0f0")
            self.label_question.pack(pady=(10, 5))

            self.entry_reponse = tk.Entry(self.master, font=("Helvetica", 14), bg="#ffffff")
            self.entry_reponse.pack(pady=5, ipady=5, ipadx=10)

            self.label_timer = tk.Label(self.master, text=f"Temps restant : {self.time_remaining} s", font=("Helvetica", 12), bg="#f0f0f0")
            self.label_timer.pack(pady=5)

            self.button_valider = tk.Button(self.master, text="Valider", command=self.valider_reponse, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief=tk.FLAT)
            self.button_valider.pack(pady=10, ipady=5, ipadx=10)

            self.progress_bar = tk.Label(self.master, text=f"Question {self.current_question + 1}/10", font=("Helvetica", 12), bg="#f0f0f0")
            self.progress_bar.pack(pady=5)

            self.score_label = tk.Label(self.master, text=f"Score : {self.score}/10", font=("Helvetica", 12), bg="#f0f0f0")
            self.score_label.pack(pady=5)

            self.generer_question()
            self.start_timer()
        else:
            messagebox.showwarning("Erreur", "Veuillez choisir un niveau de difficulté.")

    def generer_question(self):
        if self.current_question < 10:
            a = random.randint(1, 10)
            b = random.randint(1, 10)

            difficulty = self.difficulty_level.get()

            if difficulty == "Facile":
                operation = random.choice(["+", "-"])
            elif difficulty == "Moyen":
                operation = random.choice(["+", "-", "*"])
            else:
                operation = random.choice(["+", "-", "*", "/"])

            if operation == "+":
                resultat = a + b
            elif operation == "-":
                resultat = a - b
            elif operation == "*":
                resultat = a * b
            else:
                resultat = a / b

            self.reponse_correcte = resultat
            self.label_question.config(text=f"{a} {operation} {b} = ")
            self.entry_reponse.delete(0, tk.END)
            self.current_question += 1
            self.progress_bar.config(text=f"Question {self.current_question}/10")
        else:
            messagebox.showinfo("Fin du jeu", f"Votre score est de {self.score} sur 10.")
            choice = messagebox.askyesno("Fin du jeu", "Voulez-vous continuer?")
            if choice:
                self.current_question = 0
                self.score = 0
                self.score_label.config(text=f"Score : {self.score}/10")
                self.generer_question()
            else:
                self.master.destroy()

    def valider_reponse(self):
        reponse_utilisateur = self.entry_reponse.get()
        if reponse_utilisateur.isdigit():
            if float(reponse_utilisateur) == self.reponse_correcte:
                self.score += 1
                self.entry_reponse.config(bg="lightgreen")
            else:
                self.entry_reponse.config(bg="lightcoral")
            self.score_label.config(text=f"Score : {self.score}/10")
            self.generer_question()
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nombre.")

    def start_timer(self):
        def countdown():
            if self.time_remaining > 0:
                self.time_remaining -= 1
                self.label_timer.config(text=f"Temps restant : {self.time_remaining} s")
                self.master.after(1000, countdown)
            else:
                messagebox.showinfo("Fin du jeu", f"Temps écoulé ! Votre score est de {self.score} sur 10.")
                choice = messagebox.askyesno("Fin du jeu", "Voulez-vous continuer?")
                if choice:
                    self.current_question = 0
                    self.score = 0
                    self.score_label.config(text=f"Score : {self.score}/10")
                    self.generer_question()
                else:
                    self.master.destroy()
        countdown()

def main():
    root = tk.Tk()
    app = CalculApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
