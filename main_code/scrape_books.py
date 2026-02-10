import requests
from bs4 import BeautifulSoup
from datetime import date
import re

BASE_URL = "https://books.toscrape.com/"

def scrape_books():
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article", class_="product_pod")

    scrapped_date = date.today().isoformat()
    data = []

    for article in articles:
        title = article.h3.a["title"].strip()

        price_text = article.find("p", class_="price_color").text
        price_number = re.findall(r"[-+]?\d*\.\d+|\d+",price_text)[0]
        price_gbp = float(price_number)

        availability = article.find("p", class_="instock availability").text.strip()

        data.append({
            "scrapped_date": scrapped_date,
            "title": title,
            "price_gbp": price_gbp,
            "category": "books",
            "availability": availability
        })

    return data


if __name__ == "__main__":
    books = scrape_books()
    print(f"Scraped {len(books)} books")
    print(books[:3])
