import sqlite3

def stream_user_ages():
    conn = sqlite3.connect('your_database.db')  # Replace with actual DB path
    cursor = conn.cursor()
    cursor.execute('SELECT age FROM users')

    for row in cursor:
        yield row[0]  # assuming age is in the first (and only) column

    conn.close()

def calculate_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
