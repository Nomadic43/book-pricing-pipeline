import requests
import psycopg2
from datetime import date 

DB_CONFIG = {
    "host": "postgres",
    "dbname": "pricing",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}

API_URL = "https://open.er-api.com/v6/latest/GBP"

def fetch_gbp_to_inr_rate():

    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()

    #print("DEBUG:", data)
    return data["rates"]["INR"]

def insert_exchange_rate(rate):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    insert_query = """
        INSERT INTO staging_exchange_rates (
            rate_date,
            base_currency,
            target_currency,
            rate
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (rate_date)
        DO UPDATE SET rate = EXCLUDED.rate;
    """

    today = date.today()

    cur.execute(
        insert_query,
        (today, "GBP", "INR", rate)
    )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        current_rate = fetch_gbp_to_inr_rate()
        insert_exchange_rate(current_rate)
        print(f"Successfully updated! 1 GBP = {current_rate} INR")
    except Exception as e:
        print(f"An error occurred: {e}")