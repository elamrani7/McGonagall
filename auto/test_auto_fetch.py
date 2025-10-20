from app.wigor_api import fetch_schedule

def main():
    try:
        print("🔄 Connexion automatique à l’ENT...")
        courses = fetch_schedule()
        for c in courses:
            print(f"{c.day} | {c.subject} | {c.teacher} | {c.start_time}-{c.end_time} | {c.room}")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
