import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    port=3308,
    user='root',
    password='225Enya_system',
    database='alx_prodev'
)
cursor = conn.cursor()

# Insert sample users
cursor.executemany(
    'INSERT INTO users (name, age) VALUES (%s, %s)',
    [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
)

conn.commit()
conn.close()

print("Sample users inserted successfully into MySQL database.")
