import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection and return the cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no exceptions, else rollback
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        # Close connection
        self.cursor.close()
        self.conn.close()

# Usage example
if __name__ == "__main__":
    # Assume you have a SQLite DB file named 'example.db' and a 'users' table
    with DatabaseConnection('example.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
