import json
from datetime import datetime
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def create_job_offers_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS job_offers (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        date_posted DATE,
        location TEXT,
        company TEXT,
        contract_type TEXT,
        experience_level TEXT,
        salary TEXT,
        url TEXT,
        job_category TEXT,
        job_label TEXT
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table job_offers créée avec succès.")

def purge_old_offers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM job_offers;")
    conn.commit()
    cur.close()
    conn.close()
    print("🗑️ Toutes les anciennes offres ont été supprimées.")

def insert_offres_from_file(json_path: str):
    conn = get_connection()
    cur = conn.cursor()

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for offre in data.get("resultats", []):
        try:
            cur.execute("""
                INSERT INTO job_offers (
                    id, title, description, date_posted, location,
                    company, contract_type, experience_level,
                    salary, url, job_category, job_label
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                offre.get("id"),
                offre.get("intitule"),
                offre.get("description"),
                offre.get("dateCreation", "")[:10] or None,
                offre.get("lieuTravail", {}).get("libelle"),
                offre.get("entreprise", {}).get("nom"),
                offre.get("typeContratLibelle"),
                offre.get("experienceLibelle"),
                offre.get("salaire", {}).get("libelle"),
                offre.get("origineOffre", {}).get("urlOrigine"),
                offre.get("romeLibelle"),
                offre.get("appellationlibelle")
            ))
            count += 1
        except Exception as e:
            print(f"❌ Erreur sur l'offre {offre.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ {count} offres insérées dans PostgreSQL depuis {json_path}")


if __name__ == "__main__":
    create_job_offers_table()
