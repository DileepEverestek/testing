import os
from dotenv import load_dotenv
from datetime import datetime,timedelta
from typing import Optional
import jwt
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME:str = "testfast2"
    PROJECT_VERSION: str = "1.0.0"
    MYSQL_USER : str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER : str = os.getenv("MYSQL_SERVER","localhost")
    MYSQL_PORT : str = os.getenv("MYSQL_PORT",5432) # default postgres port is 5432
    MYSQL_DB : str = os.getenv("MYSQL_DB","tdd")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    SECRET_KEY = "secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1
    REFRESH_TOKEN_EXPIRE_MINUTES = 30
    DELETE_TOKEN_MINUTES = 0

settings = Settings()

#core > security.py






def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(seconds=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def refresh_token(token):
    payload = {
        "exp": datetime.utcnow() + timedelta(settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "scope": "refresh_token",
        "sub": token,
        # "iss": "cfs-account",
        # "aud": ["patient", "professional"],
    }
    print(payload['exp'])
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


def access_token_extend(token):
    payload = {
        "exp": datetime.utcnow() + timedelta(seconds=20),
        "scope": "access_token",
        "sub": token,
        # "iss": "cfs-account",
        # "aud": ["patient", "professional"],
    }
    print(payload['exp'])
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def encode_refresh_token(userid):
    """
    function is for refresh_token for 30 minutes
        Input-

                userid - active user id

        Output-
                refresh_token
    """
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes = 1),
        "scope": "refresh_token",
        "sub": userid,
        # "iss": "cfs-account",
        # "aud": ["patient", "professional"],
    }
    print(payload['exp'])
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


def decode_token(token):
    """
    function is for decode the access_token
        Input-

               Access_token

        Output-
                return user_id
    """
    try:
        jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM, verify=True)
        # return payload["sub"]
    except jwt.exceptions.ExpiredSignatureError:
        return {"Toeken time expired"}


def delete_token(token):
    payload = {
        "exp": datetime.utcnow()
               + timedelta(microseconds=1),
        "scope": "access_token",
        "sub": token,
        # "iss": "cfs-account",
        # "aud": ["patient", "professional"],
    }
    print(payload['exp'])
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)