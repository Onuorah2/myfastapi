from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() #this will copy the data we want to encode
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #this will add the current time to the 30 min of when it will expire
    to_encode.update({'exp': expire}) #this will give the meaasge that it has expired and then store it in the to_encode

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM) #you have to put the alogrithms in a bracket cause it expects a list of alogrithms
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        print(token)
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])  #decode the token sent by the user
        id: str = payload.get('user_id') #this will get the user id from auth and store it in this id and maybe decode it, i dont know

        if id is None:    #i think, if the id is not the same after decoding it
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id) #this is to make sure that the id in the token is the same as the id of the user

    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'could not validate credentials', headers= {'www-Authenticate':'Bearer'})

    token = verify_access_token(token, credentials_exception) #since we have access to the token which contains the id, we can fetch the user from the database directly
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user#this is the token for our current user







