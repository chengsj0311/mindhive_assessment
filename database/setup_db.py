import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("zus_stores.db")
cursor = conn.cursor()

# Drop table if it exists (for testing purposes)
cursor.execute("DROP TABLE IF EXISTS zus_stores")

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS zus_stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,
    address TEXT NOT NULL,
    google_maps_link TEXT
)
""")
conn.commit()

# Scrape and insert
for i in range(1, 23):
    url = f"https://zuscoffee.com/category/store/kuala-lumpur-selangor/page/{i}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    stores = soup.find_all("article", class_="post")

    for store in stores:
        # Store name
        name_tag = store.find("p", class_="elementor-heading-title")
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        # Break if we reach the Ingredients
        if name == "Ingredients":
            break

        # Address
        content_tag = store.find("div", class_="elementor-widget-theme-post-content")
        p_tag = content_tag.find("p") if content_tag else None
        address = p_tag.get_text(strip=True) if p_tag else "N/A"

        # Google Maps link
        link_tag = store.find("a", class_="premium-button", href=True)
        map_link = link_tag['href'] if link_tag else "N/A"

        print(f"Store Name: {name}")
        print(f"Address: {address}")
        print(f"Google Maps Link: {map_link}")
        print("-" * 50)

        # Insert into DB
        cursor.execute("""
            INSERT INTO zus_stores (store_name, address, google_maps_link)
            VALUES (?, ?, ?)
        """, (name, address, map_link))
        conn.commit()

# Close connection
conn.close()
