from .. import models, schemas, utils, oauth2    #double . is because all these are located in a different folder 
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import engine, Sessionlocal, get_db
from typing import  List

router = APIRouter()
tags=['user'] #this will help group our request into categories. this is just  a normal nm=ame just to know better what this file is about



@router.post('/user', status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)  #notice the response is not usercreate. this is so, so that the password is not displayed to the user
def new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  #for this user to be able to post sth, it will depend on get_current_user

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    create_user= models.User(**user.dict())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)

    return (create_user)