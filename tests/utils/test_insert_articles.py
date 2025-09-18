import sqlite3
from pathlib import Path
from nbv.utils.insert_articles import *
from nbv.utils.init_db import init_articles

def test_check_table_full():
    conn = sqlite3.connect(":memory:")

    # add empty table
    init_articles(conn)

    # table is empty
    full = check_table_full("Articles", conn)
    assert full is False

    # table is full now
    filename = Path(__file__).parent.parent / "data" / "sample_headlines.csv"
    store_articles(filename, conn)
    full = check_table_full("Articles", conn)
    assert full is True

def test_store_articles():
    conn = sqlite3.connect(":memory:")
    filename = Path(__file__).parent.parent / "data" / "sample_headlines.csv"

    #create table
    init_articles(conn)
    store_articles(filename, conn)

    c = conn.cursor()
    full = check_table_full("Articles", conn)
    assert full is True
