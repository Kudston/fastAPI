import os
import datetime 
from passlib.context import CryptContext
import jwt

PASSWORD_HASHER_PASS = os.environ["HASHING_PASSWORD"]
ALGORITHM   = "HS256"


password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def validate_password(input_password: str, db_pass: str) -> bool:
    return password_hasher.verify(input_password, db_pass)


def refreshTokenGenerator(id):
    return jwt.encode({
        'id':id,
        'iat':datetime.datetime.utcnow(),
        'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=30)
    },PASSWORD_HASHER_PASS,algorithm=ALGORITHM)

def decodeRefreshToken(token):
    return jwt.decode(token,PASSWORD_HASHER_PASS,ALGORITHM)

def accessTokenGenerator(id):
    return jwt.encode(
        {
            'id':id,
            'iat':datetime.datetime.utcnow(),
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        },PASSWORD_HASHER_PASS,ALGORITHM
    )

def decodeRefreshToken(token):
    return jwt.decode(token,PASSWORD_HASHER_PASS,ALGORITHM)

