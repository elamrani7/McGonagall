from playwright.sync_api import sync_playwright

import re

USERNAME = "hamza.elamrani"
PASSWORD = "Elamrani99."

def get_cookie_and_hash():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Étape 1 : Accès à la page CAS
        page.goto("http://ws-edt-cd.wigorservices.net", wait_until="domcontentloaded")

        # Étape 2 : Attente du formulaire
        page.wait_for_selector('input[name="username"]', timeout=10000)

        # Étape 3 : Remplissage et soumission
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')

        # Étape 4 : Attente de redirection vers WIGOR
        page.wait_for_url("**WebPsDyn.aspx**", timeout=15000)

        # Étape 5 : Récupération des cookies
        cookies = context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        # Étape 6 : Récupération du hashURL
        url = page.url
        hash_match = re.search(r"hashURL=([A-F0-9]{64,})", url)
        if not hash_match:
            hash_match = re.search(r"hashURL=([A-F0-9]{64,})", page.content())
        hash_url = hash_match.group(1) if hash_match else None

        browser.close()

        if not hash_url:
            raise Exception("❌ hashURL introuvable")

        return cookie_str, hash_url
    
def fetch_auto_login():
    return get_cookie_and_hash()

