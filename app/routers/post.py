from .. import models, schemas, utils, oauth2    #double . is because all these are located in a different folder 
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, Sessionlocal, get_db
from typing import  List, Optional

router = APIRouter()
tags=['post'] #this will help group our request into categories. this is just  a normal nm=ame just to know better what this file is about




# @router.get('/post', response_model= list[schemas.PostOut])
# def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip= 0, search: Optional[str]= ''): #the limit(10) is the default limit. youl still have to enter the main limit the the url.   skip = 0 cause we dont want to skip anything by defaullt

#     # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

#     results= db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #models.vote is the teable we want to make a joint. Post.id is the id from the post table we want to make a joint with. Vote.post_id is the id in votes table we want to join. group_ by is the way we want to group it where is id in the post is the main/head. there are 2 types of left joint(inner and outer).sqlalchemy performs inner by default but we want outer, thats why we put isouter.   we want to name the column where the number of counts per post will show, thats why we have label

#     return results


@router.get('/post/{id}', response_model= schemas.PostOut)
def get_post(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'the id: {id} does not exist')
    return post


@router.post('/post', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #this current_user= depends is what will now make  sure that the user must be logged in before creating a post
    print(current_user)
    new_post = models.Post(owner_id= current_user.id, **post.dict())    #the capital pose is the pose from the models.py whci is creating our models, table while the small is the variable where we saved out createpost.   there is no way for this create post to know that the owner owns this so we had to equate the owner_id to the current user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   #just like return *
    return(new_post)





@router.put('/post/{id}', status_code=status.HTTP_201_CREATED)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    mypost = query_post.first()

    if mypost == None:      #this first is only added bor the if statement and not the lower part. its the same for delete
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the id: {id} does not exist')
    
    if mypost.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'not authorized to perfrom request action')

    
    query_post.update(updated_post.dict(), synchronize_session=False) # we passed in our schema post.dict
    db.commit()
    return query_post.first() #we passed in a status_code for delete so this is def diff


@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'the id:{id} does not exist')

    if post.owner_id != current_user.id: #this is a check to make sure that the owner is deleting only his post and no other persons
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'not authorized to perfrom request action')
    post_query.delete(synchronize_session=False)  #the reason this has no first is so that we can delete evry post with that id
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
