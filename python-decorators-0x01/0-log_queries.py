import sqlite3
"""
Assumes 'users' table already exists in 'users.db' SQLite database and is managed externally.
"""
import functools

#### decorator to lof SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the 'query' from either args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        print(f"Executing query: {query}") # Log the query
        return func(*args, **kwargs) # Call the original function
    return wrapper

@log_queries
def fetch_all_users(query):
    # Connect to the SQLite database and fetch all users based on the provided query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

# Display the fetched users to verify everything works
print(users)
