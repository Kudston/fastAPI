from sqlalchemy.orm import Session
from  fastapi import HTTPException,status
from . import models, blogapi_schemas,blogapi_utilities,database



def get_user(db: Session, user_id: int):
    return db.query(models.User_model).filter(models.User_model.id == user_id).first()

def get_user_by_email(db:Session, user_email:str):
    return db.query(models.User_model).filter(models.User_model.email == user_email ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_model).offset(skip).limit(limit).all()


def create_user(db: Session, user: blogapi_schemas.user_create_class):
    hashed_password = blogapi_utilities.generate_password_hash
    db_user = models.User_model(username=user.username,email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_Blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()


def create_users_blog(db: Session, blog: blogapi_schemas.Blog_Schema, user_id: int):
    db_blog = models.Blog(**blog.dict(), author_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh()
    return db_blog

def get_user_blog(db:Session,  user_id:int, blog_id:int):
    return db.query(models.Blog).filter(models.Blog.author_id==user_id).filter(models.Blog.id==blog_id)

def update_blog(db:Session, update_info:blogapi_schemas.Blog_Schema, user_id:int, blog_id:int):
    user_blog_query = get_user_blog(db, user_id, blog_id)
    if user_blog_query is None:
        return None
    user_blog_query.update(update_info)
    db.commit()
    db.refresh()
    return user_blog_query


def delete_blog(db:Session, update_info:blogapi_schemas.Blog_Schema, user_id:int, blog_id:int):
    user_blog_query = get_user_blog(db, user_id, blog_id)
    if user_blog_query is None:
        return None
    db.delete(user_blog_query)
    db.commit()
    db.refresh()
    return user_blog_query
