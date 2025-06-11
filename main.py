import os
import shutil
from src.token import get_token
from src.scraper import fetch_offres
from src.s3 import upload_file_to_s3
from src.db import create_job_offers_table, insert_offres_from_file, purge_old_offers
from src.analyse import run_analysis

def clear_figures_folder():
    figures_path = "figures"
    if os.path.exists(figures_path):
        shutil.rmtree(figures_path)
    os.makedirs(figures_path)
    print("🚹 Dossier figures/ nettoyé.")

def main():
    nombres_offres = 149
    token = get_token()
    json_path = fetch_offres(token, nombres_offres)
    if not json_path:
        return

    upload_file_to_s3(json_path, f"raw/{json_path.split('/')[-1]}")
    create_job_offers_table()
    purge_old_offers()
    insert_offres_from_file(json_path)

    clear_figures_folder()
    run_analysis()

if __name__ == "__main__":
    main()
