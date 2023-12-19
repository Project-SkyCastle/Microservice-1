from fastapi import FastAPI, Request
from datetime import datetime, date
import time
import logging
from .user import User, Role
from .dbhandler import DbHandler
from .publish_sns import send_sns_message

app = FastAPI()
db = DbHandler()


# Middleware functionality: logging request details
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    with open("request_log.txt", mode="a") as reqfile:
        content = f"Method: {request.method}, Path: {request.url.path}, Response_status: {response.status_code}, Duration: {process_time}s\n"
        reqfile.write(content)
    return response


@app.get("/")
async def root():
    return {"message": "Hello SkyCastle Team"}


@app.get("/user")
async def get_all_users():
    """Fetch all users."""
    logging.info("get_all_users() called")

    sql = "SELECT user_id, email, created, role, discord_url FROM users"
    res = db.execute_with_retry(sql).fetchall()

    logging.info(res)

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
async def get_user(user_id: int):
    """Fetch the user info with user_id=user_id."""
    logging.info("get_user() called")

    sql = "SELECT user_id, email, created, role, discord_url FROM users WHERE user_id=%(user_id)s"
    res = db.execute_with_retry(sql, {"user_id": user_id}).fetchone()

    if res is None:
        logging.error("Could not find user_id=%(user_id)s", user_id)
        return None

    logging.info(res)

    return {
        "user_id": res.user_id,
        "email": res.email,
        "created": res.created,
        "role": res.role,
        "discord_url": res.discord_url,
    }


@app.get("/user/search/")
async def search_user(
    email: str = "",
    created_on_or_after: date = date(1970, 1, 1),
    role: str = "",
    discord_url: str = "",
):
    """Fetch all users matching the query string."""
    logging.info("search_user() called")

    filters = []
    params = {}

    if email != "":
        params["email"] = email
        filters.append("email=%(email)s")

    if created_on_or_after != date(1970, 1, 1):
        params["created"] = created_on_or_after
        filters.append("created>=%(created)s")

    if role != "":
        params["role"] = Role[role]
        filters.append("role=%(role)s")

    if discord_url != "":
        params["discord_url"] = discord_url
        filters.append("discord_url=%(discord_url)s")

    if len(params) == 0:
        return []

    predicates = " and ".join(filters)

    sql = (
        "SELECT user_id, email, created, role, discord_url FROM users WHERE "
        + predicates
    )
    res = db.execute_with_retry(sql, params).fetchall()

    logging.info(res)

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


@app.post("/user")
async def create_user(user: User):
    """Creates a new user and returns the user's id."""
    logging.info("create_user() called")

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
        logging.info(response)

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
                logging.info(response)
    return this_user


@app.put("/user")
async def update_user(user: User):
    """Update existing user with user_id."""
    logging.info("update_user() called")

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
        logging.info(response)

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
                logging.info(response)
    return this_user


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    """Deletes user with user_id."""
    logging.info("delete_user() called")

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
        logging.info(response)

    return {"Deleted": user_id}
