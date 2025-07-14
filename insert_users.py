import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Insert sample users
cursor.executemany(
    'INSERT INTO users (name, age) VALUES (?, ?)',
    [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
)

conn.commit()
conn.close()

# Print confirmation
print("Sample users inserted successfully.")
