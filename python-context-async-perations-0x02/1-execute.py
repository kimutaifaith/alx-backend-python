import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()

# Run the query manually without 'with'
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

context = ExecuteQuery('example.db', query, params)
context.__enter__()
results = context.result
context.__exit__(None, None, None)

for row in results:
    print(row)
