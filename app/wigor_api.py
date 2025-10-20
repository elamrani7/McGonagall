import requests
from datetime import datetime
from app.models import Course
from app.index import parse_schedule

def fetch_schedule(cookie: str, date: str = None) -> list[Course]:
    if date is None:
        date = datetime.today().strftime("%m/%d/%Y")

    url = (
        "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx"
        f"?action=posEDTLMS&serverID=C&Tel=hamza.elamrani&date={date}&hashURL=B374EC3DEACC9813449CE1BACB71EFC129841AB8BEB5A9CA07EB53B2EF1B32ED36D176E7F7CC291CF43EE6BE8A7A37EAE66B2425DC6E0019839A9A7AA02D1AEA"
    )

    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    if "Connexion" in response.text or "cas" in response.url.lower():
        raise Exception("Non authentifié : redirigé vers la page de connexion CAS.")

    if response.status_code == 200:
        html = response.text
        return parse_schedule(html)
    else:
        raise Exception(f"Erreur API : {response.status_code}")
