import mysql.connector

def stream_users_in_batches(batch_size):
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
            yield batch
            batch = []
    
    # Yield any remaining rows
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        filtered = [user for user in batch if user[3] > 25]  # 3rd loop (list comprehension)
        yield filtered

# Optional test
if __name__ == "__main__":
    for filtered_batch in batch_processing(5):
        print("Filtered batch:")
        for user in filtered_batch:
            print(user)
