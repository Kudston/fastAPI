import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_PASSWORD = os.environ['POSTGRESQL_PASSWORD']

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:{}@localhost/postgres".format(POSTGRES_PASSWORD)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
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
