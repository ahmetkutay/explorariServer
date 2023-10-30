import json
from datetime import datetime, timedelta
import jwt
from bson import ObjectId
from fastapi import HTTPException

from Configs.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, ENCRYPT_PASSWORD
from Helpers.Encryptions import EncryptionHandler
from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None
    iat: float | None = None
    exp: float | None = None
    sub: str | None = None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"iat": datetime.utcnow()})
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def encrypt_user_data(user):
    user_id_str = str(ObjectId(user['_id']))
    encrypted_user_id = EncryptionHandler(ENCRYPT_PASSWORD).encrypt(user_id_str)
    access_token_data = {
        "sub": encrypted_user_id,
        "data": {
            "username": user["username"],
            "email": user["email"]
        }
    }
    json_serializable_data = json.loads(json.dumps(access_token_data, default=str))
    return json_serializable_data
