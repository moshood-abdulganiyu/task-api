import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

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


# def get_all_tasks():
def get_all_tasks(done=None, search=None, sort=None):
    with connection() as conn:
        return conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()


def get_task(task_id):
    with connection() as conn:
        return conn.execute(
            "SELECT * FROM tasks WHERE id = %s", (task_id,)
        ).fetchone()

    
def create_task(title):
    with connection() as conn:
        return conn.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
            (title, False),
        ).fetchone()


def update_task(task_id, title, done):
    with connection() as conn:
        return conn.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
            (title, done, task_id),
        ).fetchone()


def delete_task(task_id):
    with connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        return cursor.rowcount > 0
