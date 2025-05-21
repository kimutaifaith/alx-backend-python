import time
import sqlite3 
import functools

query_cache = {}

# ✅ with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Adjust path if needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("🔁 Using cached result for query.")
            return query_cache[query]
        print("💾 Caching result for query.")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# ✅ Function using cache and db connection
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users
