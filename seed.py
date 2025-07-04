
# Import the mysql.connector library to allow Python to connect to MySQL databases
import mysql.connector

# Define a function to connect to the MySQL server (not to a specific database yet)
def connect_db():
    """
    Connects to the MySQL server using your credentials.
    Returns the connection object if successful, or None if it fails.
    """
    try:
        # Create a connection object with your MySQL server details
        # Replace 'root' and 'password' with your actual MySQL username and password
        connection = mysql.connector.connect(
            host='127.0.0.1',      # The server address (localhost means your own computer)
            user='root',           # Your MySQL username
            password='',    # Your MySQL password
            port=3307  # The port number MySQL is running on (default is usually 3306, but here it's set to 3307 for this example)
        )
        # If connection is successful, return the connection object
        return connection
    except mysql.connector.Error as err:
        # If there is an error, print it and return None
        print(f"Error: {err}")
        return None

# This block runs only if you execute this script directly (not when you import it)
if __name__ == "__main__":
    conn = connect_db()  # Try to connect to the MySQL server
    if conn:
        print("Connection successful!")
        conn.close()  # Always close the connection when done
    else:
        print("Connection failed.")
