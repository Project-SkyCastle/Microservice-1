import psycopg

with psycopg.connect(
    user="postgres",
    host="database-1.czm7bnq0spbp.us-east-2.rds.amazonaws.com",
    port="5432",
) as conn:
    with conn.cursor() as cur:
        with open("db/users.sql") as users:
            sql = users.read()
            cur.execute(sql)
    