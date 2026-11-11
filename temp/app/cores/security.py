from pwdlib import PasswordHash
import jwt
from datetime import datetime, timezone, timedelta
from app.cores.config import settings

password_hash = PasswordHash.recommended()

# Password Hashing
def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

# JWT Generation
def create_access_token(user_id : int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token

def decode_access_token(token : str) -> int | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        return None