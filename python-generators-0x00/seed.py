import mysql.connector
import uuid
import pandas as pd
import os
def connect_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
    except mysql.connector.Error as err:
        print("❌ Failed to connect to MySQL server:", err)
        raise

def create_database(connection):
    try:
        print(">> Attempting to create database...")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        print("✅ Database 'ALX_prodev' created or already exists.")
    except mysql.connector.Error as err:
        print("❌ Failed to create database:", err)
    finally:
        cursor.close()


def connect_to_prodev():
    return mysql.connector.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'ALX_prodev'
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL,
        INDEX(email)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()       
    
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        name, email, age = row

        # Check if email already exists
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            continue  # Skip duplicates

        # Insert new row
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (user_id, name, email, age)
        )
    connection.commit()
    cursor.close()



def main():
    print(">>> Starting seeding process...")

    try:
        # Connect and setup database
        print(">> Connecting to MYsQL server..")
        conn = connect_db()
        print("✅ Connected to MySQL server.")

        print(">> Creating database...")
        create_database(conn)
        print("✅ Database checked/created.")
        conn.close()

        # Connect to ALX_prodev and create table
        prodev_conn = connect_to_prodev()
        print("✅ Connected to ALX_prodev database.")
        create_table(prodev_conn)
        print("✅ Table checked/created.")

        # Check if CSV file exists
        csv_path = "user_data.csv"
        print(f">> Checking if CSV exists at {csv_path}...")
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found at: {csv_path}")
            return
        else:
            print(f"✅ Found CSV: {csv_path}")

        # Load CSV data
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} records from CSV")
        print(df.head())  # Show sample data
        records = df[['name', 'email', 'age']].values.tolist()

        # Insert data
        insert_data(prodev_conn, records)
        print("✅ Data inserted into user_data table.")

        print("🎉 Database seeded successfully.")
        prodev_conn.close()

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)

if __name__ == "__main__":
    main()
