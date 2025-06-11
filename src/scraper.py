import requests
import os
import json
from datetime import datetime
from src.token import get_token
from src.config import SEARCH_URL

def fetch_offres(token: str, nombres_offres=150, save_dir="data") -> str | None:
    headers = {"Authorization": f"Bearer {token}"}
    all_results = []
    step = 150
    start = 0

    while len(all_results) < nombres_offres:
        end = min(start + step - 1, nombres_offres - 1)
        params = {
            "motsCles": "data",
            "departement": "75",
            "rayon": "10",
            "range": f"{start}-{end}",
            "sort": 1
        }

        response = requests.get(SEARCH_URL, headers=headers, params=params)
        if response.status_code in [200, 206]:
            data = response.json()
            offres = data.get("resultats", [])
            if not offres:
                break
            all_results.extend(offres)
            start += step
        else:
            print("❌ Erreur API :", response.status_code, response.text)
            return None

    if not all_results:
        print("❌ Aucune donnée récupérée.")
        return None

    os.makedirs(save_dir, exist_ok=True)
    filename = datetime.now().strftime(f"{save_dir}/offres_%Y%m%d_%H%M%S.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"resultats": all_results}, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(all_results)} offres sauvegardées dans : {filename}")
    return filename

# Test standalone
if __name__ == "__main__":
    token = get_token()
    fetch_offres(token, nombres_offres=300)
