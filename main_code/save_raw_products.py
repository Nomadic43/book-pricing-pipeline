import psycopg2 
from scrape_books import scrape_books

DB_CONFIG = {
    "host":"postgres",
    "dbname":"pricing",
    "user":"airflow",
    "password":"airflow",
    "port":5432
}

def insert_raw_products(products):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    insert_query = """
        INSERT INTO raw_products(
            scrapped_date,
            title,
            price_gbp,
            category,
            availability
        )
        VALUES(%s,%s,%s,%s,%s)
    """

    for product in products:
        cur.execute(
            insert_query,
            (
                product["scrapped_date"],
                product["title"],
                product["price_gbp"],
                product["category"],
                product["availability"]
            )
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    products = scrape_books()
    insert_raw_products(products)
    print(f"Inserted {len(products)} records into raw_products")