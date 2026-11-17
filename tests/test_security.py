
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from jose import jwt
from app.core.config import settings


def test_password_hashing():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password():
    hashed = hash_password("TestPassword123")

    assert not verify_password("WrongPassword123", hashed)


def test_access_token_creation():
    token = create_access_token({"sub": "1"})

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    assert payload["sub"] == "1"
    assert "exp" in payload
