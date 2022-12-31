import os
import datetime 
from passlib.context import CryptContext
from jose import jwt
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends


token_collect = OAuth2PasswordBearer(tokenUrl='login')

configuration_file = dotenv_values('.env')

PASSWORD_HASHER_PASS = configuration_file.get('DATABASE_HASHING_PASSWORD')
ALGORITHM   = configuration_file.get('DATABASE_ALGORITHM')
ACCESS_TOKEN_EXPIRATION = int(configuration_file.get('ACCESS_TOKEN_EXPIRATION'))
REFRESH_TOKEN_EXPIRATION = int(configuration_file.get('REFRESH_TOKEN_EXPIRATION'))

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
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=REFRESH_TOKEN_EXPIRATION)
        },PASSWORD_HASHER_PASS,algorithm=ALGORITHM)
    except:
        return None
def decodeRefreshToken(token):
    return jwt.decode(token,PASSWORD_HASHER_PASS,ALGORITHM)
    


def verify_refresh_token(token:str,error_exception):
    try:
        token_data = decodeRefreshToken(token)
        id: int = token_data.get('id')
        if id is None:
            raise error_exception
        user_id = id
    except:
        raise error_exception
    return user_id

def get_user_id(token:str=Depends(token_collect)):
    payload = verify_refresh_token(token,error_exception=HTTPException(status_code=status.HTTP_400_BAD_REQUEST,headers={'WWW-Authenticate': 'Bearer'}))
    return payload