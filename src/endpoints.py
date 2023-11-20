from fastapi import FastAPI
from datetime import datetime
import uuid
from .user import User
from .dbhandler import DbHandler
from psycopg.rows import class_row
from .publish_sns import send_sns_message

app = FastAPI()
db = DbHandler()


@app.get("/")
async def root():
    return {"message": "Hello SkyCastle Team"}


@app.get("/user/")
async def get_all_users():
    """Fetch all users."""

    sql = "SELECT user_id, email, created, role, discord_url FROM users"

    with db.conn.cursor(row_factory=class_row(User)) as cur:
        cur.execute(sql)
        res = cur.fetchall()

        return [
            {
                "user_id": row.user_id,
                "email": row.email,
                "created": row.created,
                "role": row.role,
                "discord_url": row.discord_url,
            }
            for row in res
        ]


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    """Fetch the user info with user_id=user_id."""

    sql = "SELECT user_id, email, created, role, discord_url FROM users WHERE user_id=%(user_id)s"

    with db.conn.cursor(row_factory=class_row(User)) as cur:
        cur.execute(sql, {"user_id": user_id})
        res = cur.fetchone()

        if res is None:
            print(f"Could not find user_id={user_id}")
            return None

        return {
            "user_id": res.user_id,
            "email": res.email,
            "created": res.created,
            "role": res.role,
            "discord_url": res.discord_url,
        }


@app.post("/user/")
async def create_user(user: User):

    """Creates a new user and returns the user's id."""

    sql = ("INSERT into users(user_id, email, created, role, discord_url) "
           "VALUES (%(user_id)s, %(email)s, %(created)s, %(role)s, %(discord_url)s) RETURNING *")
    sql1 = "SELECT discord_url FROM users where role = 'ADMIN'"

    with db.conn.cursor(row_factory=class_row(User)) as cur:
        user_id = uuid.uuid4()
        created = datetime.now()
        try:
            cur.execute(
                sql,
                {
                    "user_id": user_id,
                    "email": user.email,
                    "created": created,
                    "role": user.role,
                    "discord_url": user.discord_url,
                },
            )
            db.conn.commit()
            this_user = cur.fetchone()

        except Exception as ex:
            db.conn.rollback()
            return ex


        if user.discord_url is not None:
            # get notifications
            message_attributes = {
                'webhook_url': {
                    'DataType': 'String',
                    'StringValue': user.discord_url
                },
            }

            response = send_sns_message("Hi! You have just created a new user as " + user.role + " on SkyCastle.",
                                        message_attributes)
            print(response)

        # notify admins when a new analyst join
        if user.role == "ANALYST":
            cur.execute(sql1)
            res = cur.fetchall()

            for row in res:
                if row.discord_url is not None:
                    message_attributes = {
                        'webhook_url': {
                            'DataType': 'String',
                            'StringValue': row.discord_url
                        },
                    }

                    response = send_sns_message("Hi SkyCastle admin! A new ANALYST has joined on SkyCastle.",
                                                message_attributes)
                    print(response)
        return this_user

@app.put("/user/")
async def update_user(user: User):
    """Update existing user with user_id."""
    sql = "UPDATE users SET role=%(role)s, discord_url=%(discord_url)s WHERE user_id=%(user_id)s RETURNING *"
    sql1 = "SELECT discord_url FROM users where role = 'ADMIN'"
    sql2 = "SELECT role, discord_url FROM users WHERE user_id=%(user_id)s"

    with db.conn.cursor(row_factory=class_row(User)) as cur:
        # get the user which wants to be updated
        cur.execute(sql2, {"user_id": user.user_id})
        res = cur.fetchone()
        if res is None:
            return "User doesn't exist"

        try:
            cur.execute(sql, {"user_id": user.user_id, "role": user.role, "discord_url": user.discord_url})
            db.conn.commit()
            this_user = cur.fetchone()

        except Exception as ex:
            print(ex)
            db.conn.rollback()
            return ex

        if user.discord_url is not None:
            # get notifications
            message_attributes = {
                'webhook_url': {
                    'DataType': 'String',
                    'StringValue': user.discord_url
                },
            }

            response = send_sns_message("Hi! You have just updated a user on SkyCastle.",
                                        message_attributes)
            print(response)

        # notify admins when a new analyst join
        if user.role == "ANALYST":
            cur.execute(sql1)
            res = cur.fetchall()

            for row in res:
                if row.discord_url is not None:
                    message_attributes = {
                        'webhook_url': {
                            'DataType': 'String',
                            'StringValue': row.discord_url
                        },
                    }

                    response = send_sns_message("Hi SkyCastle admin! A new ANALYST has joined on SkyCastle.",
                                                    message_attributes)
                    print(response)
        return this_user


@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    """Deletes user with user_id."""

    sql = "DELETE FROM users WHERE user_id=%(user_id)s"

    sql1 = "SELECT role, discord_url FROM users WHERE user_id=%(user_id)s"


    with db.conn.cursor(row_factory=class_row(User)) as cur:
        # get the user which wants to be deleted
        cur.execute(sql1, {"user_id": user_id})
        res = cur.fetchone()
        if res is None:
            return "User doesn't exist"

        try:
            #delete the user
            cur.execute(sql, {"user_id": user_id})
            db.conn.commit()

        except Exception as ex:
            db.conn.rollback()
            return ex

        #delete sucessfully, notification part
        if res.discord_url is not None:
            # get notifications
            message_attributes = {
                'webhook_url': {
                    'DataType': 'String',
                    'StringValue': res.discord_url
                },
            }

            response = send_sns_message("Hi! You have just deleted a user with role " + res.role + " on SkyCastle.",
                                        message_attributes)
            print(response)

        return {"Deleted": user_id}
