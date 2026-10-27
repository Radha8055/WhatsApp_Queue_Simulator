import sqlite3

DB_NAME = "messages.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (

            id TEXT PRIMARY KEY,

            sender TEXT NOT NULL,

            receiver TEXT NOT NULL,

            message TEXT NOT NULL,

            status TEXT NOT NULL

        )
    """)

    conn.commit()

    conn.close()