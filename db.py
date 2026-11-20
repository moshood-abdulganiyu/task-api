import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

import db_sqlite

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

SEED_TASKS = [
    ("Learn what an API is", True),
    ("Build my first endpoint", False),
    ("Push my code to GitHub", False),
]


def connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db():
    db_sqlite.init_db()
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) AS count FROM tasks").fetchone()["count"]
        if count == 0:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)", SEED_TASKS
                )


get_all_tasks = db_sqlite.get_all_tasks
get_task = db_sqlite.get_task
create_task = db_sqlite.create_task
update_task = db_sqlite.update_task
delete_task = db_sqlite.delete_task
