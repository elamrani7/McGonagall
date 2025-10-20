import tkinter as tk
from tkinter import messagebox
from app.wigor_api import fetch_schedule
from datetime import datetime, timedelta

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
HEURES = [f"{h:02d}:00" for h in range(9, 19)]  # 09:00 à 18:00

def heure_range(start, end):
    fmt = "%H:%M"
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    heures = []
    while start_dt < end_dt:
        heures.append(start_dt.strftime(fmt))
        start_dt += timedelta(hours=1)
    return heures

def run_app():
    root = tk.Tk()
    root.title("McGonagallPlanner")
    root.geometry("1170x600")
    root.resizable(False, False)

    # Titre
    tk.Label(root, text="🧙‍♀️ McGonagallPlanner", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Champ cookies
    cookies_frame = tk.Frame(root)
    cookies_frame.pack(pady=5)
    tk.Label(cookies_frame, text="Tous les cookies :").pack(side=tk.LEFT)
    cookies_entry = tk.Entry(cookies_frame, width=100)
    cookies_entry.pack(side=tk.LEFT)

    # 🖼️ Canvas scrollable pour la grille
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame, width=980, height=450)
    v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")

    # En-têtes de colonnes (jours)
    tk.Label(scrollable_frame, text="Heure", width=10, borderwidth=1, relief="solid", font=("Helvetica", 10, "bold")).grid(row=0, column=0)
    for j, jour in enumerate(JOURS):
        tk.Label(scrollable_frame, text=jour, width=25, borderwidth=1, relief="solid", font=("Helvetica", 10, "bold")).grid(row=0, column=j+1)

    # Cases vides initiales
    cell_refs = {}
    for i, heure in enumerate(HEURES):
        tk.Label(scrollable_frame, text=heure, width=10, borderwidth=1, relief="solid", font=("Helvetica", 9)).grid(row=i+1, column=0)
        for j, jour in enumerate(JOURS):
            cell = tk.Label(
                scrollable_frame,
                text="",
                width=25,
                height=4,
                borderwidth=1,
                relief="solid",
                wraplength=180,
                justify="center",
                font=("Helvetica", 9)
            )
            cell.grid(row=i+1, column=j+1)
            cell_refs[(jour, heure)] = cell

    # Bouton de chargement
    def load_schedule():
        cookie = cookies_entry.get().strip()
        if not cookie:
            messagebox.showerror("Erreur", "Veuillez coller vos cookies.")
            return
        try:
            courses = fetch_schedule(cookie)
            if not courses:
                messagebox.showinfo("Planning", "Aucun cours trouvé.")
                return

            # Nettoyer la grille
            for cell in cell_refs.values():
                cell.config(text="", bg="white")

            # Placer les cours
            for c in courses:
                heures_cours = heure_range(c.start_time, c.end_time)
                for h in heures_cours:
                    if (c.day, h) in cell_refs:
                        # ✅ Salle affichée une seule fois
                        if c.room in c.teacher:
                            contenu = f"{c.subject}\n{c.teacher}\n{c.classe}"
                        else:
                            contenu = f"{c.subject}\n{c.teacher}\n{c.classe}\n{c.room}"
                        cell_refs[(c.day, h)].config(text=contenu, bg="#d0e0ff")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le planning : {e}")

    tk.Button(root, text="Charger emploi du temps", command=load_schedule).pack(pady=5)

    root.mainloop()
