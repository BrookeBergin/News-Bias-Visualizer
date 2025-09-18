import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "instance", "news.db")

def check_table_exists(tablename, conn=None):
    close_conn = False
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        close_conn = True

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
    count = c.fetchone()[0]
    if count == 0:
        print("Table does not exist")
        result =  False
    else:
        print(tablename + " table exists.")
        result =  True

    if close_conn:
        conn.close()

    return result

# Connect to Sqlite3 server
def init_articles(conn=None):
    print("Creating table")
    try:
        close_conn = False
        if conn is None:
            conn = sqlite3.connect(DB_PATH)
            close_conn = True

        c = conn.cursor()
        # create table
        sql_create_statement = """CREATE TABLE Articles (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                source TEXT NOT NULL,
                                title TEXT NOT NULL,
                                url TEXT,
                                published_at TEXT,
                                sentiment_score REAL,
                                UNIQUE(title, source)
                                ); """
        c.execute(sql_create_statement)

        conn.commit()

        if close_conn:
            conn.close()

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)