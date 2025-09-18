import sqlite3
from nbv.utils.init_db import init_articles, check_table_exists

def test_check_table_exists():
    conn = sqlite3.connect(":memory:")

    # table doesn't exist
    exists = check_table_exists("Articles", conn)
    assert exists is False

    # table exists now
    init_articles(conn)
    exists = check_table_exists("Articles", conn)
    assert exists is True

def test_init_articles():
    conn = sqlite3.connect(":memory:")
    init_articles(conn)

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Articles'")
    count = c.fetchone()[0]
    assert count != 0
