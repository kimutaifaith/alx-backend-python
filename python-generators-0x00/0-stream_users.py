import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    for row in cursor:
        yield row  # Yield one row at a time

    cursor.close()
    connection.close()

# Optional: If you want to test the generator
if __name__ == "__main__":
    for user in stream_users():
        print(user)
