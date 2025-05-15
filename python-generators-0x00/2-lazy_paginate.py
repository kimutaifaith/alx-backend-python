import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a page of users using SELECT * and pagination.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    # Using the exact required string
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def lazy_paginate(page_size):
    """
    Generator that yields user data pages lazily.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
