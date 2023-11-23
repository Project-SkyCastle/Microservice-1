import psycopg
from datetime import datetime

dummy_data = [
    {
        # "user_id": 1,
        "email": "sol@skycastle.com",
        "created": datetime.strptime(
            "2023-11-15T13:48:39.916672", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ANALYST",
        "discord_url": "https://discord.com/api/webhooks/1173294248074956950/3Tl0JWq4xzN1RVsyuCDjD7KCv1WMsxh96IJ9nbBnTivo95ZhGUpTjxIpaEOju02dTkpV",
    },
    {
        # "user_id": 2,
        "email": "selena@test.com",
        "created": datetime.strptime(
            "2023-11-15T14:25:44.077431", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ANALYST",
        "discord_url": "https://discord.com/api/webhooks/1173294248074956950/3Tl0JWq4xzN1RVsyuCDjD7KCv1WMsxh96IJ9nbBnTivo95ZhGUpTjxIpaEOju02dTkpV",
    },
    {
        # "user_id": 3,
        "email": "selena_admin1@test.com",
        "created": datetime.strptime(
            "2023-11-20T08:51:20.082750", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ADMIN",
        "discord_url": None,
    },
    {
        # "user_id": 4,
        "email": "selena_admin2@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:00:56.023277", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ADMIN",
        "discord_url": None,
    },
    {
        # "user_id": 5,
        "email": "selena_admin3@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:02:11.143012", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ADMIN",
        "discord_url": None,
    },
    {
        # "user_id": 6,
        "email": "selena_admin4@test.com",
        "created": datetime.strptime(
            "2023-11-15T14:29:24.775525", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ADMIN",
        "discord_url": None,
    },
    {
        # "user_id": 7,
        "email": "selena_admin5@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:16:30.988594", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ADMIN",
        "discord_url": None,
    },
    {
        # "user_id": 8,
        "email": "selena_admin6@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:17:02.442432", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ANALYST",
        "discord_url": None,
    },
    {
        # "user_id": 9,
        "email": "selena_admin7@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:19:29.202099", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ANALYST",
        "discord_url": None,
    },
    {
        # "user_id": 10,
        "email": "selena_admin8@test.com",
        "created": datetime.strptime(
            "2023-11-20T09:19:29.202099", "%Y-%m-%dT%H:%M:%S.%f"
        ),
        "role": "ANALYST",
        "discord_url": None,
    },
]

with psycopg.connect(
    user="postgres",
    host="database-1.czm7bnq0spbp.us-east-2.rds.amazonaws.com",
    port="5432",
    autocommit=True,
) as conn:
    with conn.cursor() as cur:
        with open("db/users.sql") as users:
            sql = users.read()
            cur.execute(sql)

        insert = (
            "INSERT into users (email, created, role, discord_url) "
            "VALUES (%(email)s, %(created)s, %(role)s, %(discord_url)s)"
        )
        for row in dummy_data:
            cur.execute(insert, row)
            print(row)
