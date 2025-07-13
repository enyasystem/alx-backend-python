##import sqlite3
##import functools

#### decorator to lof SQL queries
#def log_queries(func):
 #   @functools.wraps(func)
  #  def wrapper(*args, **kwargs):
        # Extract the 'query' from either args or kwargs
   #     query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
    #    print(f"Executing query: {query}") # Log the query
     #   return func(*args, **kwargs) # Call the original function
    #return wrapper

#@log_queries
#def fetch_all_users(query):
    # Connect to the SQLite database and fetch all users based on the provided query
 #   conn = sqlite3.connect('users.db')
  #  cursor = conn.cursor()
  #  cursor.execute(query)
   # results = cursor.fetchall()
    #conn.close()
    #return results

#### fetch users while logging the query
#users = fetch_all_users(query="SELECT * FROM users")


import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL query - assume it's the first positional argument
        if args:
            print(f"[LOG] Executing SQL Query: {args[0]}")
        else:
            print("[LOG] No SQL query found in arguments.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
