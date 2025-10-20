import re
from bs4 import BeautifulSoup
from app.models import Course


def parse_schedule(html: str) -> list[Course]:
    soup = BeautifulSoup(html, "html.parser")
    courses = []

    # 🗓️ Jours fixes (3 cours par jour)
    jours_fixes = ["Lundi"] * 3 + ["Mardi"] * 3 + ["Mercredi"] * 3 + ["Jeudi"] * 3 + ["Vendredi"] * 3
    jour_index = 0

    # 📚 Extraire les cours
    for div in soup.find_all("div", class_="innerCase"):
        try:
            table = div.select_one("div.BackGroundCase table.TCase")
            if not table:
                continue

            rows = table.find_all("tr")
            subject = teacher = classe = room = "Inconnu"
            start = end = "00:00"

            for row in rows:
                tds = row.find_all("td")
                for td in tds:
                    class_name = td.get("class", [])
                    if "TCase" in class_name:
                        subject = td.get_text(strip=True)
                    elif "TCProf" in class_name:
                        lines = td.get_text(separator="\n", strip=True).split("\n")
                        teacher = lines[0] if len(lines) > 0 else "Inconnu"
                        classe = lines[1] if len(lines) > 1 else ""
                    elif "TChdeb" in class_name:
                        time_text = td.get_text(strip=True)
                        if "-" in time_text:
                            start, end = [t.strip() for t in time_text.split("-")]
                    elif "TCSalle" in class_name:
                        room = td.get_text(strip=True)

            # 🧠 Fusion prof + salle
            teacher_full = f"{teacher} — {room}" if room != "Inconnu" else teacher

            # 🧠 Jour fixe
            day = jours_fixes[jour_index] if jour_index < len(jours_fixes) else "Inconnu"
            jour_index += 1

            courses.append(Course(day, subject, teacher_full, start, end, room, classe))

        except Exception as e:
            print(f"Erreur de parsing d’un cours : {e}")
            continue

    return courses
