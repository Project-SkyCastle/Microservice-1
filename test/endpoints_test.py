from fastapi.testclient import TestClient
from src.endpoints import app
from unittest.mock import MagicMock, patch
from src.user import User, Role
from datetime import datetime

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello SkyCastle Team"}


@patch("src.endpoints.db")
def test_get_all_users(db):
    user = User.model_validate(
        {
            "user_id": 1,
            "email": "email",
            "created": datetime(2023, 12, 1),
            "role": Role.ADMIN,
            "discord_url": "discord_url",
        }
    )
    cursor = MagicMock()
    cursor.fetchall.return_value = [user]
    db.execute_with_retry.return_value = cursor

    response = client.get("/user/")
    assert response.status_code == 200
    assert db.execute_with_retry.called_with(
        "SELECT user_id, email, created, role, discord_url FROM users"
    )
    assert response.json() == [user.model_dump(mode="json")]


@patch("src.endpoints.db")
def test_get_user(db):
    user = User.model_validate(
        {
            "user_id": 1,
            "email": "email",
            "created": datetime(2023, 12, 1),
            "role": Role.ADMIN,
            "discord_url": "discord_url",
        }
    )
    cursor = MagicMock()
    cursor.fetchone.return_value = user
    db.execute_with_retry.return_value = cursor

    response = client.get("/user/1")
    assert response.status_code == 200
    assert db.execute_with_retry.called_with(
        "SELECT user_id, email, created, role, discord_url FROM users WHERE user_id=%(user_id)s",
        {"user_id": 1},
    )
    assert response.json() == user.model_dump(mode="json")
