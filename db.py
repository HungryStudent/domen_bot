from contextlib import closing
import sqlite3

database = "database.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY autoincrement, name TEXT, offer_id INT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY autoincrement, url TEXT, project_id INTEGER, is_active BOOL)")
        connection.commit()


def create_project(name, offer_id, domain):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO projects(name, offer_id) VALUES (?, ?)", (name, offer_id))
        project_id = cursor.lastrowid
        cursor.execute("INSERT INTO urls(url, project_id, is_active) VALUES (?, ?, true)",
                       (domain, project_id))
        connection.commit()


def get_projects():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT id, name, offer_id FROM projects")
        return cursor.fetchall()


def get_project(project_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT name, offer_id FROM projects WHERE id = ?", (project_id,))
        return cursor.fetchone()


def delete_project(project_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        cursor.execute("DELETE FROM urls WHERE project_id = ?", (project_id,))
        connection.commit()


def add_domain(url, project_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO urls(url, project_id, is_active) VALUES (?, ?, false)", (url, project_id))
        connection.commit()


def change_domain(project_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("DELETE FROM urls WHERE is_active = true and project_id = ?", (project_id,))
        cursor.execute("SELECT url, id FROM urls WHERE project_id = ? ORDER BY id LIMIT 1", (project_id,))
        data = cursor.fetchone()
        if data is None:
            return "error"
        cursor.execute("UPDATE urls SET is_active = true WHERE id = ?", (data[1],))
        connection.commit()
        return data[0]


def get_current_url(project_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT url FROM urls WHERE is_active = true and project_id = ?", (project_id,))
        return cursor.fetchone()
