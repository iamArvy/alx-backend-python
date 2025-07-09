import time
import sqlite3 
import functools

# === with_db_connection decorator ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === retry_on_failure decorator ===
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed due to: {e}")
                    if attempts < retries:
                        time.sleep(delay)
                    else:
                        print("[RETRY] All attempts failed.")
                        raise
        return wrapper
    return decorator

# === Usage ===
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# === Run ===
users = fetch_users_with_retry()
print(users)
