import psycopg


class DbHandler:
    def __init__(self):
        self.conn = psycopg.connect(
            user="postgres",
            host="database-1.czm7bnq0spbp.us-east-2.rds.amazonaws.com",
            port="5432",
        )

        print("Connected")
