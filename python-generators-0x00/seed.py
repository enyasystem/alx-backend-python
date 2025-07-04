def insert_data(connection, data):
    """
    Inserts a new user record into the user_data table.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        data (dict): A dictionary containing user data (user_id, name, email, age).
    """
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);
    """, (data['user_id'], data['name'], data['email'], data['age']))
    connection.commit()
    cursor.close()

# Function to insert all users from a CSV file
def insert_all_from_csv(connection, csv_file):
    """
    Reads user data from a CSV file and inserts each row into the user_data table.
    """
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'age': int(row['age'])
            }
            insert_data(connection, data)
# Import the csv library to handle CSV file reading
# Add this import at the top of your file
import csv

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
            port=3307,  # The port number MySQL is running on (default is usually 3306, but here it's set to 3307 for this example)
            database='ALX_prodev'  # Optional: specify a database to connect to
        )
        # If connection is successful, return the connection object
        return connection
    except mysql.connector.Error as err:
        # If there is an error, print it and return None
        print(f"Error: {err}")
        return None


def create_table(connection):
    """
    Creates the user_data table if it does not exist.
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            age INT NOT NULL,
            INDEX (user_id)
        );
    """)
    connection.commit()
    cursor.close()



# Function to clear the user_data table
def clear_table(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_data;")
    connection.commit()
    cursor.close()

# This block runs only if you execute this script directly (not when you import it)
if __name__ == "__main__":
    conn = connect_db()  # Try to connect to the MySQL server and ALX_prodev DB
    if conn:
        create_table(conn)  # Create the user_data table if it doesn't exist
        clear_table(conn)  # Clear the table before inserting new data
        insert_all_from_csv(conn, 'user_data.csv')  # Insert all users from the new CSV
        print("Connection successful, table checked/created, and data inserted!")
        conn.close()  # Always close the connection when done
    else:
        print("Connection failed.")
        

def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    """
    cursor = connection.cursor()  # Get a cursor to execute SQL
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")  # SQL to create DB
    cursor.close()

# def insert_data(connection, data):
    """
    Inserts a new user record into the user_data table.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        data (dict): A dictionary containing user data (name, email, age).
    """
    # cursor = connection.cursor()
    # cursor.execute("""
    #     INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);
    # """, (data['user_id'], data['name'], data['email'], data['age']))
    # connection.commit()
    # cursor.close()
