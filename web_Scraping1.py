import requests
from bs4 import BeautifulSoup
import csv

# URL and Headers
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

# Mapping rating words to numeric values
rating_mapping = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Open CSV file for writing
with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])  # CSV Header

    page = 1  # Start from page 1
    while True:
        url = base_url.format(page)  # Format the page number in the URL
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("🚫 No more pages to scrape!")
            break  # Stop when there are no more pages

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        if not books:
            break  # Stop if no books are found

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = rating_mapping.get(book.p["class"][1], 0)  # Convert rating

            writer.writerow([title, price, rating])  # Write book details to CSV

            print(f"📖 {title} - {price} - ⭐ {rating}")  # Print extracted data

        page += 1  # Move to the next page

print("✅ Scraping complete! Data saved to books_data.csv")
