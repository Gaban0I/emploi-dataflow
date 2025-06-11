import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def run_analysis():
    load_dotenv()
    os.makedirs("figures", exist_ok=True)

    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT", 5432)

    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_sql("SELECT * FROM job_offers", con=engine)

    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["contract_type"] = df["contract_type"].fillna("Inconnu")
    df["location"] = df["location"].fillna("Non précisé")

    # 1. Répartition des types de contrat
    plt.figure(figsize=(10, 5))
    df["contract_type"].value_counts().plot(kind="bar", color="skyblue", title="Répartition des contrats")
    plt.ylabel("Nombre d'offres")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("figures/contract_distribution.png")
    plt.close()

    # 2. Nombre d'offres par jour
    plt.figure(figsize=(12, 5))
    df["date_posted"].dt.date.value_counts().sort_index().plot(kind="bar", color="orange", title="Offres par date de publication")
    plt.ylabel("Nombre d'offres")
    plt.tight_layout()
    plt.savefig("figures/offres_par_date.png")
    plt.close()

    # 3. Top 10 des localisations
    plt.figure(figsize=(10, 5))
    df["location"].value_counts().head(10).plot(kind="barh", color="green", title="Top 10 des localisations")
    plt.xlabel("Nombre d'offres")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("figures/top_localisations.png")
    plt.close()

    # 4. Évolution mensuelle du nombre d’offres
    df["month_posted"] = df["date_posted"].dt.to_period("M")
    monthly_counts = df["month_posted"].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    monthly_counts.plot(kind="line", marker="o")
    plt.title("Évolution mensuelle du nombre d'offres")
    plt.ylabel("Nombre d'offres")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("figures/evolution_offres.png")
    plt.close()

    print("✅ Graphiques générés :")
    print("- figures/contract_distribution.png")
    print("- figures/offres_par_date.png")
    print("- figures/top_localisations.png")
    print("- figures/evolution_offres.png")

if __name__ == "__main__":
    run_analysis()
