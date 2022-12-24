from pydantic import BaseModel,EmailStr

class user_base_class(BaseModel):
    username:str
    email:EmailStr
    
class user_create_class(user_base_class):
    password:str

class User_model(user_base_class):
    id:int
    is_active:bool=False
    
    class config:
        orm_mode = True

class login_model(BaseModel):
    email:str
    password:str

    class config:
        orm_mode = True

class Blog_Schema(BaseModel):
    title:str
    content:str
    
    class config:
        orm_mode = True

