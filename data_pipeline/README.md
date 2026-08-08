# Data Pipeline Module

## Overview

This module implements a complete data pipeline using Books to Scrape.

The pipeline performs:

1. Web scraping using requests and BeautifulSoup
2. Data cleaning and type conversion
3. GBP to INR currency conversion
4. SQLite database creation and loading
5. SQL querying
6. pandas analysis using pd.read_sql() and pd.merge()

## Data Source

Website: Books to Scrape

The project scrapes the first 5 pages of the All Products catalogue.

Total books collected: 100

The dataset contains books from multiple categories.

## Technologies Used

- Python
- requests
- BeautifulSoup
- pandas
- SQLite
- sqlite3

## Currency Conversion

The project uses the required fixed baseline conversion rate:

**1 GBP = 105.50 INR**

This is a project-defined fixed rate. No external currency API is used.

## Data Cleaning

### Price

The GBP currency symbol and unexpected encoding characters were removed before converting the price to float.

Example:

£51.77 → 51.77

### Rating

Text ratings were converted to integers:

- One → 1
- Two → 2
- Three → 3
- Four → 4
- Five → 5

### Availability

The availability text was converted into a Boolean value:

- In stock → True
- Otherwise → False

### Category

Unexpected category text such as "Add a comment" was treated as "Unknown" instead of being stored as a valid category.

## Database Design

The SQLite database contains two normalized tables.

### categories

- category_id - Primary Key
- category_name - Unique category name

### books

- book_id - Primary Key
- title
- price_gbp
- price_inr
- rating
- in_stock
- category_id - Foreign Key referencing categories

The relationship between the tables is:

categories.category_id → books.category_id

## SQL Queries

The project includes queries demonstrating:

1. SELECT and WHERE
2. ORDER BY
3. LIMIT
4. DISTINCT
5. BETWEEN
6. JOIN

Query strings and their outputs are saved in:

sql_queries_output.txt

## pandas Validation

The JOIN result was read from SQLite using:

pd.read_sql()

The same JOIN was reproduced using:

pd.merge()

Both results were compared using pandas and produced:

True

This confirms that the SQL JOIN and pandas merge produced equivalent results.

## How to Run

Install required packages:

pip install requests beautifulsoup4 pandas

Run the Python script:

python data_pipeline/scrape_books.py

The script creates the SQLite database and loads the scraped data.

## Output Files

- scrape_books.py
- books.db
- sql_queries_output.txt
- README.md 