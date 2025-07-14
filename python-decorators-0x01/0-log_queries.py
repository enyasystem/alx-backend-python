import sqlite3
import functools

# Decorator to log SQL queries before execution
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the 'query' argument from either kwargs or args
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        print(f"Executing query: {query}")  # Log the query
        return func(*args, **kwargs)        # Call the original function
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
