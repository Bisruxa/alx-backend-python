import mysql.connector

class ExecuteQuery:
    def __init__(self, host, user, password, database, query, params=()):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False  
query = "SELECT * FROM users WHERE age > %s"
params = (25,)

with ExecuteQuery(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database",
    query=query,
    params=params
) as result:
    for row in result:
        print(row)
