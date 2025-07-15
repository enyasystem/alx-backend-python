<<<<<<< HEAD

import sqlite3
import functools
from datetime import datetime
=======
import sqlite3
import functools
>>>>>>> be458976cc93ecb21de0b4a9ac3737ee52d74c01

# Decorator to log SQL queries before execution
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the 'query' argument from either kwargs or args
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
<<<<<<< HEAD
        # Log the query with a timestamp
        print(f"[{datetime.now()}] Executing query: {query}")
=======
        print(f"Executing query: {query}")  # Log the query
>>>>>>> be458976cc93ecb21de0b4a9ac3737ee52d74c01
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
