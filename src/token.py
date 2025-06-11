import requests
from src.config import CLIENT_ID, CLIENT_SECRET, SCOPE, TOKEN_URL

def get_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Jeton d'accès obtenu.")
        return token
    else:
        raise Exception(f"❌ Erreur lors de l'obtention du token : {response.status_code} - {response.text}")
