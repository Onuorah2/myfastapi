from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): #this is the same as user_credentials: schemas.UserLogin. it will retrieve the useres credentials and store it in user_credentials
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #its supposed to be user_credentials.email but that oauth2passwordrequestform stores its own email in a username so it has to match

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    access_token = oauth2.create_access_token(data={'user_id':user.id})  #the data we want to pass into the token is ithe user.id

    return {'access_token': access_token, 'token_type': 'bearer'}
