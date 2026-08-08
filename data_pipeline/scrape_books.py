import requests
from bs4 import BeautifulSoup
import pandas as pd

GBP_TO_INR = 105.50

all_books = []

for page in range(1, 6):

    url = f"http://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    print("Page:", page, "Books:", len(books))

    for book in books:

        title = book.h3.a["title"]

        price_text = book.select_one(".price_color").text.strip()
        price_text = price_text.replace("£", "").replace("Â", "")
        price_gbp = float(price_text)

        rating_text = book.select_one(".star-rating")["class"][1]

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        rating = rating_map.get(rating_text)

        availability = book.select_one(".availability").text.strip()
        in_stock = "In stock" in availability

        price_inr = price_gbp * GBP_TO_INR

        # Get individual book page
        book_link = book.h3.a["href"]
        book_url = "http://books.toscrape.com/catalogue/" + book_link.replace("../", "")

        book_response = requests.get(book_url)
        book_response.encoding = "utf-8"

        book_soup = BeautifulSoup(book_response.text, "html.parser")

        breadcrumb = book_soup.select("ul.breadcrumb li")

        if len(breadcrumb) >= 3:
            category = breadcrumb[2].get_text(strip=True)
        else:
            category = "Unknown"

        if category == "Add a comment":
            category = "Unknown"

        all_books.append({
            "title": title,
            "price_gbp": price_gbp,
            "rating": rating,
            "in_stock": in_stock,
            "price_inr": price_inr,
            "category": category
        })

df = pd.DataFrame(all_books)

print("\nTotal books collected:", len(df))

print("\nFirst 5 books:")
print(df.head())

print("\nCategories:")
print(df["category"].unique())

print("\nNumber of categories:", df["category"].nunique())

print("\nData types:")
print(df.dtypes)

import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")

conn.commit()

print("\nDatabase and tables created successfully!")

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON")

# Clear old data if the script is run again
cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM categories")

# Insert categories
categories = df["category"].unique()

for category in categories:
    cursor.execute(
        "INSERT INTO categories (category_name) VALUES (?)",
        (category,)
    )

# Create a category name -> category_id mapping
cursor.execute("SELECT category_id, category_name FROM categories")

category_map = {
    name: category_id
    for category_id, name in cursor.fetchall()
}

# Insert books
for _, row in df.iterrows():

    cursor.execute("""
        INSERT INTO books
        (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row["title"],
        row["price_gbp"],
        row["price_inr"],
        row["rating"],
        int(row["in_stock"]),
        category_map[row["category"]]
    ))

conn.commit()

print("Data inserted successfully!")

# Check number of records
cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

print("Books in database:", book_count)
print("Categories in database:", category_count)

conn.close()


# =========================
# SQL QUERIES
# =========================

conn = sqlite3.connect("books.db")

queries = {

    "Query 1 - SELECT and WHERE":
    """
    SELECT title, price_gbp, rating
    FROM books
    WHERE rating >= 4
    """,

    "Query 2 - ORDER BY":
    """
    SELECT title, price_gbp
    FROM books
    ORDER BY price_gbp DESC
    """,

    "Query 3 - LIMIT":
    """
    SELECT title, price_gbp
    FROM books
    ORDER BY price_gbp DESC
    LIMIT 10
    """,

    "Query 4 - DISTINCT":
    """
    SELECT DISTINCT category_name
    FROM categories
    ORDER BY category_name
    """,

    "Query 5 - BETWEEN":
    """
    SELECT title, price_gbp, rating
    FROM books
    WHERE price_gbp BETWEEN 20 AND 40
    """,

    "Query 6 - JOIN":
    """
    SELECT
        books.title,
        books.price_gbp,
        books.rating,
        books.in_stock,
        categories.category_name
    FROM books
    JOIN categories
        ON books.category_id = categories.category_id
    ORDER BY books.rating DESC, books.price_gbp DESC
    LIMIT 10
    """
}

# Save queries and outputs
with open("sql_queries_output.txt", "w", encoding="utf-8") as file:

    for query_name, query in queries.items():

        print("\n" + "=" * 60)
        print(query_name)
        print("=" * 60)

        print(query)

        result = pd.read_sql(query, conn)

        print(result)

        file.write("\n" + "=" * 60 + "\n")
        file.write(query_name + "\n")
        file.write("=" * 60 + "\n")
        file.write(query + "\n")
        file.write("\nOUTPUT:\n")
        file.write(result.to_string(index=False))
        file.write("\n")

conn.close()

print("\nAll SQL queries executed successfully!")
print("SQL query outputs saved to sql_queries_output.txt")

# =========================
# PD.READ_SQL AND PD.MERGE
# =========================

conn = sqlite3.connect("books.db")

# JOIN query
join_query = """
SELECT
    books.book_id,
    books.title,
    books.price_gbp,
    books.price_inr,
    books.rating,
    books.in_stock,
    categories.category_id,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id
ORDER BY books.rating DESC, books.price_gbp DESC
LIMIT 10
"""

# Read JOIN result using pd.read_sql()
sql_join_df = pd.read_sql(join_query, conn)

print("\nJOIN result using pd.read_sql():")
print(sql_join_df)

# Read the two tables separately
books_df = pd.read_sql("SELECT * FROM books", conn)
categories_df = pd.read_sql("SELECT * FROM categories", conn)

# Reproduce the JOIN using pd.merge()
merge_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

# Select the same columns and apply the same sorting/limit
merge_df = merge_df[
    [
        "book_id",
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_id",
        "category_name"
    ]
]

merge_df = merge_df.sort_values(
    by=["rating", "price_gbp"],
    ascending=[False, False]
).head(10)

merge_df = merge_df.reset_index(drop=True)

print("\nJOIN result using pd.merge():")
print(merge_df)

# Check whether both results are equivalent
sql_result = sql_join_df.reset_index(drop=True)

print("\nAre pd.read_sql() and pd.merge() results equivalent?")
print(sql_result.equals(merge_df))

conn.close()