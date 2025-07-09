import time
import sqlite3 
import functools

# === Connection manager ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Cache dictionary ===
query_cache = {}

# === Cache decorator ===
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]
        else:
            print("[CACHE] Executing and caching result.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

# === Query function with caching ===
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# === Run: first call caches, second uses cache ===
users = fetch_users_with_cache(query="SELECT * FROM users")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
