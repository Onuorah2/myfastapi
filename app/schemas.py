from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:  #this is to convert it to a dict or something like that
        orm_mode = True

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut    #this will return userout

    class Config:  #this is to convert it to a dict or something like that
        orm_mode = True

class PostOut(BaseModel):
    Post: Post  #the first p is intentionally capital and its gotten from myschemas(the second one or the post class in models). the second post is from Post class up there
    votes: int   #becase there is no clolumn for votes in the Post up there, thats why e did not work

    class Config:  
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:  #this is to convert it to a dict or something like that
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):  #the user has to send back the token
    access_token: str
    token_type: str

class TokenData(BaseModel):  #this is the data we passed into our token when we were creating it
    id: Optional[str] = None #its not a must the user will enter it

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   #le is less than or equal to 1. this is the value of the vote. 1 is for vote amd 0 is for unlike

