from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User_model(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean,default=False)
    user_blogs = relationship("Blog", back_populates="blog_author")
    
    created_on = Column(DateTime,nullable=True)
    updated_on = Column(DateTime,nullable=True)
    
class Blog(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    blog_author = relationship("User_model", back_populates="user_blogs")
    
    created_on = Column(DateTime,nullable=False)
    updated_on = Column(DateTime,nullable=False)
    
class refresh_token(Base):
    __tablename__  = "refreshTokens"
    
    user_id = Column(Integer,primary_key=True, index=True)
    token  = Column(String, unique=True)
    
class access_token(Base):
    __tablename__ = "accessTokens"
    
    user_id = Column(Integer, primary_key=True, index =True)
    token  = Column(String, unique=True)
