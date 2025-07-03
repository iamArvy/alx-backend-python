import sqlite3

def paginate_users(page_size, offset):
    conn = sqlite3.connect('your_database.db')  # Replace with your DB path
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users LIMIT ? OFFSET ?', (page_size, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
