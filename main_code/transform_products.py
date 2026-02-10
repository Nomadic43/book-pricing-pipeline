import psycopg2
import hashlib 
import re 

DB_CONFIG = {
    "host": "postgres",
    "dbname": "pricing",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}

def extract_availability_count(text):
   match = re.search(r"\d+",text)
   return int(match.group()) if match else 0

# test_string = "There are 42 items available"
# result = extract_availability_count(test_string)
# print(result)

def get_price_tier(price_inr):
   if price_inr < 500:
      return "cheap"
   elif price_inr < 1500:
      return "moderate"
   else:
      return "expensive"
   
def generate_product_id(title,category,price_gbp):
   raw = f"{title}|{category}|{price_gbp}"
   return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def transform_and_load_products():
   conn = psycopg2.connect(**DB_CONFIG)
   cur = conn.cursor()

   cur.execute("""
        SELECT rate, rate_date
        FROM staging_exchange_rates
        ORDER BY rate_date DESC
        LIMIT 1
    """)
   
   row =   cur.fetchone()

   if row is None:
      raise Exception("No exchange rate found in staging_exchange_rates")
   
   rate, rate_date = row 

   cur.execute("""
        SELECT title, price_gbp, category, availability
        FROM raw_products
    """)
   rows = cur.fetchall()

   insert_query = """
        INSERT INTO products (
            product_id,
            title,
            category,
            availability_count,
            price_gbp,
            price_inr,
            price_tier,
            rate_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id)
        DO UPDATE SET
            price_inr = EXCLUDED.price_inr,
            price_tier = EXCLUDED.price_tier,
            rate_date = EXCLUDED.rate_date;
    """
   
   for title, price_gbp, category, availability in rows:
        title_clean = title.strip()
        category_clean = category.strip().lower()

        availability_count = extract_availability_count(availability)
        price_inr = round(price_gbp * rate, 2)
        price_tier = get_price_tier(price_inr)

        product_id = generate_product_id(
            title_clean, category_clean, price_gbp
        )

        cur.execute(
            insert_query,
            (
                product_id,
                title_clean,
                category_clean,
                availability_count,
                price_gbp,
                price_inr,
                price_tier,
                rate_date
            )
        )
   conn.commit()
   cur.close()
   conn.close()


if __name__ == "__main__":
    transform_and_load_products()
    print("Products table successfully updated")
