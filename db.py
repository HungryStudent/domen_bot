from contextlib import closing
import sqlite3

database = "database.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY autoincrement, url TEXT, is_active BOOL)")
        connection.commit()


def add_domain(url):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO urls(url, is_active) VALUES (?, false)", (url,))
        connection.commit()


def change_domain():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("DELETE FROM urls WHERE is_active = true")
        cursor.execute("SELECT url, id FROM urls ORDER BY id LIMIT 1")
        data = cursor.fetchone()
        if data is None:
            return "error"
        cursor.execute("UPDATE urls SET is_active = true WHERE id = ?", (data[1],))
        connection.commit()
        return data[0]



def get_current_url():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT url FROM urls WHERE is_active = true")
        return cursor.fetchone()