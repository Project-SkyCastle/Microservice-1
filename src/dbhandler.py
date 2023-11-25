import psycopg
from psycopg.rows import class_row
from .user import User


class DbHandler:
    def __init__(self):
        self.reconnect()

    def reconnect(self) -> None:
        self.conn = psycopg.connect(
            user="postgres",
            host="database-1.czm7bnq0spbp.us-east-2.rds.amazonaws.com",
            port="5432",
            autocommit=True,
        )

        print("Connected")

    def execute_with_retry(
        self, sql: str, args: dict = None, retry: int = 3
    ) -> psycopg.Cursor:
        while retry:
            try:
                cur = self.conn.cursor(row_factory=class_row(User))
                cur.execute(sql, args)
                return cur

            except Exception as ex:
                retry -= 1
                self.reconnect()

                if retry == 0:
                    raise ex
