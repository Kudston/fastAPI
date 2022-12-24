from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
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

@app.post("/sign-in/",response_class=None)
def SignIn(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = blog_CRUD.get_user_by_email(db,form_data.email)
    #check if user exist
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Invalid credentials provided')
    hashed_pass = User_model.hashed_password
    #check password
    if not blogapi_utilities.validate_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials provided")
    #return refresh token
    refresh_token = blogapi_utilities.refreshTokenGenerator(db_user.id)
    return refresh_token
        

@app.get("/users/", response_model=None)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = blog_CRUD.get_users(db, skip=skip, limit=limit)
    if len(users) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No record found for specified')
    return users


@app.get("/user/{user_id}/", response_model=None)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = blog_CRUD.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/blog-create/", response_model=None)#blogapi_schemas.Blog_Schema)
def create_blogs_for_user(user_id: int, blog: blogapi_schemas.Blog_Schema, db: Session = Depends(database.get_db)):
    return blog_CRUD.create_users_blog(db=db, blog=blog, user_id=user_id)


@app.get("/blogs/", response_model=None)#List[blogapi_schemas.Blog_Schema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    blogs = blog_CRUD.get_Blogs(db, skip=skip, limit=limit)
    return blogs

# @app.put("/blogs/{blog_id}/update", response_model=None)#blogapi_schemas.Blog_Schema)
# def update_blog(update_info:blogapi_schemas.Blog_Schema, user_id:int, blog_id:int, db:Session = Depends(database.get_db)):
#     blog = blog_CRUD.update_blog(update_info=update_info, user_id=user_id, blog_id=blog_id, db=db)
#     if blog is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog not found')
#     return blog

# @app.delete("/blogs/{id}/", response_model=None)
# def delete_blog(user_id:int, blog_id:int, db: Session= Depends (database.get_db)):
#     blog = blog_CRUD.delete_blog(db=db,user_id=user_id, blog_id=blog_id)
#     if blog is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {blog_id} id does not exist')
#     return "successfully deleted blog"

