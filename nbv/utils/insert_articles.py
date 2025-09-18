import sqlite3
import csv
from nbv.utils.init_db import *
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "instance", "news.db")

def check_table_full(tablename, conn=None):
    close_conn = False
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        close_conn = True

    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM {tablename}")
    count = c.fetchone()[0]

    if count == 0:
        print("Table is empty.")
        result = False
    else:
        print("Table contains data.")
        result = True

    if close_conn:
        conn.close()

    return result


def store_articles(filename, conn=None) -> None:
    print("Storing articles...")
    try:
        close_conn = False
        if conn is None:
            conn = sqlite3.connect(DB_PATH)
            close_conn = True

        c = conn.cursor()
        batch_size = 20000
        batch = []

        start_time = time.time()

        # insert article info into table
        # open csv file
        with open(filename, 'r', encoding='utf8', errors='replace', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            stored = 0
            for row in csv_reader:
                date, publication, headline, url = row

                # skip rows with empty source or title
                if not publication.strip() or not headline.strip():
                    continue

                batch.append((publication, headline, url, date))
                if len(batch) >= batch_size:
                    c.executemany(
                        "INSERT OR IGNORE INTO Articles (source, title, url, published_at) VALUES (?, ?, ?, ?)", batch)
                    conn.commit()
                    stored += len(batch)
                    print(f"Stored {stored} rows")
                    batch = []

            if batch:
                c.executemany(
                    "INSERT OR IGNORE INTO Articles (source, title, url, published_at) VALUES (?, ?, ?, ?)", batch)
                conn.commit()
                stored += len(batch)
                print(f"Stored {stored} rows")

        end_time = time.time()
        print(f"Process finished in {end_time - start_time:.2f} seconds")

        if stored == 0:
            print("No new articles found; none stored.")
        else:
            print("Stored " + str(stored) + " articles successfully.")

        if close_conn:
            conn.close()

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)