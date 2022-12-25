from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, Request
from sqlalchemy.orm import Session

from blogAPI import blog_CRUD, models, blogapi_schemas,database,blogapi_utilities

from .database import SessionLocal, engine


app = FastAPI(version='15.0.3')


models.Base.metadata.create_all(bind=engine)

@app.post("/sign-up/", response_model=None)
def SignUp(user: blogapi_schemas.user_create_class, db: Session = Depends(database.get_db)):
    db_user = blog_CRUD.get_user_by_email(db, user_email=user.email)
    
    if db_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return blog_CRUD.create_user(db=db, user=user)

@app.post('/login', summary="enter email as username", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = blog_CRUD.get_user_by_email(db=db, user_email=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.hashed_password
    if not blogapi_utilities.validate_password(form_data.password,hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    return {
        "access_token": blogapi_utilities.accessTokenGenerator(user.id),
        "refresh_token":blogapi_utilities.refreshTokenGenerator(user.id) 
    }   

@app.get("/users/", response_model=None)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = blog_CRUD.get_users(db, skip=skip, limit=limit)
    if len(users) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No record found for specified')
    return users


@app.get("/user/{user_id}/", response_model=None,status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = blog_CRUD.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/blog-create/",summary="send refresh_token with form", response_model=None, status_code=status.HTTP_201_CREATED)#blogapi_schemas.Blog_Schema)
def create_blogs_for_user(blog:blogapi_schemas.Blog_Schema, refresh_token:str, db: Session = Depends(database.get_db)):
    user_id = blogapi_utilities.decodeRefreshToken(refresh_token)
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'token not valid')
    user_id = user_id.get('id')
    return blog_CRUD.create_users_blog(db=db, blog=blog, user_id=user_id)

@app.get("/user_blogs/", response_model=None, status_code=status.HTTP_200_OK)
def get_user_blog(refresh_token:str, db: Session = Depends(database.get_db)):
    id = blogapi_utilities.decodeRefreshToken(refresh_token)
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'token not valid')
    blogs = blog_CRUD.get_user_blogs(db=db,user_id=id.get('id'))
    return blogs


@app.get("/blogs/", response_model=None, status_code=status.HTTP_200_OK)#List[blogapi_schemas.Blog_Schema])
def get_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    blogs = blog_CRUD.get_Blogs(db, skip=skip, limit=limit)
    return blogs

@app.put("/blogs/{blog_id}/update", response_model=None)
def update_blog(update_info:blogapi_schemas.Blog_Schema, blog_id:int, refresh_token:str, db:Session = Depends(database.get_db)):
    id = blogapi_utilities.decodeRefreshToken(refresh_token)
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'token not valid')
    c_blog = db.query(models.Blog).filter(models.Blog.author_id==id.get('id'), models.Blog.id==blog_id).first()
    
    if c_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id does not exist')
    
    return blog_CRUD.update_blog(update_info=update_info, user_id=id.get('id'), blog_id=blog_id, db=db)
    

@app.delete("/blogs/{id}/", response_model=None)
def delete_blog(refresh_token:str, blog_id:int, db: Session= Depends (database.get_db)):
    id = blogapi_utilities.decodeRefreshToken(refresh_token)
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'token not valid')
    
    c_blog = db.query(models.Blog).filter(models.Blog.author_id==id.get('id'), models.Blog.id==blog_id).first()
    if c_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id does not exist')
        
    blog = blog_CRUD.delete_blog(db=db,user_id=id.get('id'), blog_id=blog_id)
    return blog

