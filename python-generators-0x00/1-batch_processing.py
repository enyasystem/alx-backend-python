import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields user records in batches from the user_data table.
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
    while True:
        # Fetch a batch of rows
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows
    # Close the cursor and connection when done
    cursor.close()
    conn.close()
