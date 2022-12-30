from sqlalchemy.orm import Session
from  fastapi import HTTPException,status,Response
from . import models, blogapi_schemas,blogapi_utilities,database
from datetime import datetime
from uuid import uuid4

def generate_newId(object):
    id  = 0
    while True:
        try:
            obj = object[id][id]
            id +=1
        except:
            break
        
    
def get_user(db: Session, user_id: int):
    return db.query(models.User_model).filter(models.User_model.id == user_id).first()

def get_user_by_email(db:Session, user_email:str):
    return db.query(models.User_model).filter(models.User_model.email == user_email ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_model).offset(skip).limit(limit).all()


def create_user(db: Session, user: blogapi_schemas.user_create_class):
    hashed_password = blogapi_utilities.generate_password_hash(user.password)
    current_time = datetime.utcnow()
    id = generate_newId(db.query(models.User_model).all())
    db_user = models.User_model(id=id, username=user.username, email=user.email, hashed_password=hashed_password, created_on=current_time, updated_on=current_time)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_Blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()


def create_users_blog(db: Session, blog: blogapi_schemas.Blog_Schema, user_id: int):
    current_time = datetime.utcnow()
    blogs = db.query(models.Blog).all()
    id = generate_newId(blogs)
    db_blog = models.Blog(id=id,**blog.dict(),author_id=user_id, created_on=current_time, updated_on=current_time)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_user_blog(db:Session,  user_id:int, blog_id:int):
    return db.query(models.Blog).filter(models.Blog.author_id==user_id).filter(models.Blog.id==blog_id)
def get_user_blogs(db:Session, user_id:int):
    
    return db.query(models.Blog).filter(models.Blog.author_id==user_id).all()

def update_blog(db:Session, update_info:blogapi_schemas.Blog_Schema, user_id:int, blog_id:int):
    user_blog_query = db.query(models.Blog).filter(models.Blog.author_id==user_id, models.Blog.id==blog_id)
    user_blog = user_blog_query.first()
    if user_blog is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    update_info = update_info.dict()
    update_info['updated_on'] = datetime.utcnow()
    update = user_blog_query.update(update_info, synchronize_session=False)
    db.commit()
    return (user_blog_query.first())


def delete_blog(db:Session, user_id:int, blog_id:int):
    user_blog_query = db.query(models.Blog).filter(models.Blog.author_id==user_id, models.Blog.id==blog_id)
    
    deleted = user_blog_query.delete(synchronize_session=False)
    db.commit()
    if deleted>0:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST) 
