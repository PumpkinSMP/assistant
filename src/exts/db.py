import sqlite3


def get_connection():
    return sqlite3.connect("sqlite3.db")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY NOT NULL,
            author_id INTEGER NOT NULL,
            suggestion TEXT NOT NULL,
            status TEXT NOT NULL,
            link TEXT NOT NULL,
            note TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_new_suggestion_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT MAX(id) FROM suggestions
        """
    )
    result = cursor.fetchone()
    conn.close()
    try:
        new_id = result[0] + 1
    except TypeError:
        new_id = 1
    return new_id


def insert_suggestion(author_id: int, suggestion: str, status: str, link: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO suggestions (author_id, suggestion, status, link)
        VALUES (?, ?, ?, ?)
        """,
        (author_id, suggestion, status, link),
    )
    conn.commit()
    conn.close()


def get_suggestion(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM suggestions WHERE id = ?
        """,
        (id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result


def get_all_suggestions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM suggestions
        """,
    )
    result = cursor.fetchall()
    conn.close()
    return result


def get_suggestions(author_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT FROM suggestions WHERE author_id = ?
        """,
        (author_id,),
    )
    result = cursor.fetchall()
    conn.close()
    return result


def update_suggestion(id: int, status: str, note: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE suggestions SET status = ?, note = ? WHERE id = ?
        """,
        (status, note, id),
    )
    conn.commit()
    conn.close()
