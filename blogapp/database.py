import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")

POSTGRES_PASSWORD = config.get("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = "sqlite:///./blogapp.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:{}@localhost/postgres".format('postgrespass')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()