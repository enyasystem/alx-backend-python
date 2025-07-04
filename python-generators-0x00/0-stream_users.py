# Import the MySQL connector library
import mysql.connector

# Define the generator function
def stream_users():
    """
    Generator that yields user records one by one from the user_data table.
    """
    # Connect to the MySQL database (update credentials/port if needed)
    conn = mysql.connector.connect(
        host='127.0.0.1',      # Database server address
        user='root',           # MySQL username
        password='',           # MySQL password (empty if none)
        port=3307,             # MySQL port (change if your server uses a different port)
        database='ALX_prodev'  # Database name
    )
    # Create a cursor that returns each row as a dictionary
    cursor = conn.cursor(dictionary=True)
    # Execute a query to select all user records
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    # Loop through the cursor and yield each row (as a dict)
    for row in cursor:
        yield row
    # Close the cursor and connection when done
    cursor.close()
    conn.close()
