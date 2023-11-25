from fastapi import FastAPI
from datetime import datetime
from .user import User
from .dbhandler import DbHandler
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
    res = db.execute_with_retry(sql).fetchall()
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
    res = db.execute_with_retry(sql, {"user_id": user_id}).fetchone()

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
    sql = (
        "INSERT into users(email, created, role, discord_url) "
        "VALUES (%(email)s, %(created)s, %(role)s, %(discord_url)s) RETURNING *"
    )

    this_user = db.execute_with_retry(
        sql,
        {
            "email": user.email,
            "created": datetime.now(),
            "role": user.role,
            "discord_url": user.discord_url,
        },
    ).fetchone()

    if user.discord_url is not None:
        # get notifications
        message_attributes = {
            "webhook_url": {"DataType": "String", "StringValue": user.discord_url},
        }

        response = send_sns_message(
            "Hi! You have just created a new user as " + user.role + " on SkyCastle.",
            message_attributes,
        )
        print(response)

    # notify admins when a new analyst join
    if user.role == "ANALYST":
        sql1 = "SELECT discord_url FROM users where role = 'ADMIN'"
        res = db.execute_with_retry(sql1).fetchall()

        for row in res:
            if row.discord_url is not None:
                message_attributes = {
                    "webhook_url": {
                        "DataType": "String",
                        "StringValue": row.discord_url,
                    },
                }

                response = send_sns_message(
                    "Hi SkyCastle admin! A new ANALYST has joined on SkyCastle.",
                    message_attributes,
                )
                print(response)
    return this_user


@app.put("/user/")
async def update_user(user: User):
    """Update existing user with user_id."""

    sql = "UPDATE users SET role=%(role)s, discord_url=%(discord_url)s WHERE user_id=%(user_id)s RETURNING *"
    sql1 = "SELECT discord_url FROM users where role = 'ADMIN'"

    this_user = db.execute_with_retry(
        sql,
        {
            "user_id": user.user_id,
            "role": user.role,
            "discord_url": user.discord_url,
        },
    ).fetchone()

    if this_user is None:
        return "User doesn't exist"

    if user.discord_url is not None:
        # get notifications
        message_attributes = {
            "webhook_url": {"DataType": "String", "StringValue": user.discord_url},
        }

        response = send_sns_message(
            "Hi! You have just updated a user on SkyCastle.", message_attributes
        )
        print(response)

    # notify admins when a new analyst join
    if user.role == "ANALYST":
        res = db.execute_with_retry(sql1).fetchall()

        for row in res:
            if row.discord_url is not None:
                message_attributes = {
                    "webhook_url": {
                        "DataType": "String",
                        "StringValue": row.discord_url,
                    },
                }

                response = send_sns_message(
                    "Hi SkyCastle admin! A new ANALYST has joined on SkyCastle.",
                    message_attributes,
                )
                print(response)
    return this_user


@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    """Deletes user with user_id."""

    sql = "DELETE FROM users WHERE user_id=%(user_id)s returning *"

    deleted_user = db.execute_with_retry(sql, {"user_id": user_id}).fetchone()
    if deleted_user is None:
        return "User doesn't exist"

    # delete sucessfully, notification part
    if deleted_user.discord_url is not None:
        # get notifications
        message_attributes = {
            "webhook_url": {
                "DataType": "String",
                "StringValue": deleted_user.discord_url,
            },
        }

        response = send_sns_message(
            "Hi! You have just deleted a user with role "
            + deleted_user.role
            + " on SkyCastle.",
            message_attributes,
        )
        print(response)

    return {"Deleted": user_id}
