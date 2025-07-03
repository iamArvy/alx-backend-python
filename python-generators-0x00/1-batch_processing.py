import sqlite3

def stream_users_in_batches(batch_size):
    conn = sqlite3.connect('your_database.db')  # Replace with actual DB
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    conn.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25
        filtered = [user for user in batch if user[2] > 25]  # assuming age is at index 2
        yield filtered
