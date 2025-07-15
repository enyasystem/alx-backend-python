import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='225Enya_system',
        port=3308,
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()

def average_user_age():
    """
    Calculates and prints the average age of users using the generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    avg = total / count if count else 0
    print(f"Average age of users: {avg}")

if __name__ == "__main__":
    average_user_age()
