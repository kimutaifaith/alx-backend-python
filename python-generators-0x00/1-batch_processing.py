import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Yields batches of user records from the database.
    Each batch contains up to `batch_size` rows.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    batch = []
    for row in cursor:  # 1st loop
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # yield generator used here
            batch = []

    if batch:
        yield batch  # yield remaining records

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch of users and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        # 3rd loop: using generator expression instead of list comprehension
        for user in (u for u in batch if u[3] > 25):  # age is at index 3
            yield user  # yield generator used here
