import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches users from the database starting at the given offset.
    Returns a list of users up to the page_size.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    query = "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def lazy_paginate(page_size):
    """
    Generator that lazily fetches and yields user data in pages.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:  # one loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # yield generator used here
        offset += page_size
