import os
import datetime 
from passlib.context import CryptContext
from jose import jwt
from dotenv import dotenv_values
from .config import settings

configuration_file = dotenv_values('.env')
PASSWORD_HASHER_PASS = 'this_isMypasswordHasher'
ALGORITHM   = "HS256"

print(settings.DATABASE_ALGORITHM)


password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def validate_password(input_password: str, db_pass: str) -> bool:
    return password_hasher.verify(input_password, db_pass)


def refreshTokenGenerator(id):
    try:
        return jwt.encode({
            'id':id,
            'iat':datetime.datetime.utcnow(),
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=30)
        },PASSWORD_HASHER_PASS,algorithm=ALGORITHM)
    except:
        return None
def decodeRefreshToken(token):
    try:
        return jwt.decode(token,PASSWORD_HASHER_PASS,ALGORITHM)
    except:
        return None
    
def accessTokenGenerator(id):
    return jwt.encode(
        {
            'id':id,
            'iat':datetime.datetime.utcnow(),
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        },PASSWORD_HASHER_PASS,ALGORITHM
    )

def decodeaccessToken(token):
    try:
        return jwt.decode(token,PASSWORD_HASHER_PASS,ALGORITHM)
    except:
        return None

