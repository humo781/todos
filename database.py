import sqlite3

def connect_db():
    return sqlite3.connect('todo.db')


def create_table():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')


def get_all_tasks():
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM todo')
        return cursor.fetchall()


def get_task_by_id(task_id):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM todo WHERE id = ?', (task_id,))
        return cursor.fetchone()


def create_task(task):
    with connect_db() as conn:
        cursor = conn.execute('INSERT INTO todo (task) VALUES (?)', (task,))
        conn.commit()
        return cursor.lastrowid


def update_task(task_id, task, completed):
    with connect_db() as conn:
        conn.execute('UPDATE todo SET task = ?, completed = ? WHERE id = ?', (task, completed, task_id))
        conn.commit()


def delete_task(task_id):
    with connect_db() as conn:
        conn.execute('DELETE FROM todo WHERE id = ?', (task_id,))
        conn.commit()


