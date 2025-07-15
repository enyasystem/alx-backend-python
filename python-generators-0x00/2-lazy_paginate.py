seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that yields user records in pages of a specified size.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

import sys

try:
    for page in lazy_pagination(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
