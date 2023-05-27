from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=['vote'])

@router.post('/vote', status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post= db.query(models.Post).filter(models.Post.id == vote.post_id).first()   #this is to check make sure they re not voting on a post that does not exist
    if not post:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f'this post with {vote.post_id} does not exist')


    vote_query= db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)#post.id == vote.post_id. the vote.post-id is the schemas where the user will enter the id of the post which will then be compared with the one in the database. this one is to check wheather there is already a vote for this specific id. the second condition is to check that the user is in the database and has voted before

    found_vote= vote_query.first()

    if (vote.dir == 1):    #dir= 1 means its been liked
        if found_vote:    #if the user already liiked a post he cant like it again
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f'user {current_user.id} has already voted on {vote.post_id}')
    
        new_vote = models.Vote(post_id= vote.post_id, user_id= current_user.id)    #this will append the vote.post_id to the vote_id in the database and for the other too. this line is an else, i dont know why they did not type it
        db.add(new_vote)
        db.commit()
        return {'message': 'succesfully voted'}

    else:
        if not found_vote:  #iff there is vote
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'user {current_user.id} has already voted on {vote.post_id}')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{'message': 'seccessfully deleted vote'}



    


    



