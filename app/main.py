from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)  #this will help create all out models

app= FastAPI()

origins= ['*'] #this means every single domain can send an api request to my domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )



app.include_router(post.router)  #from router = APIRouter().that app = fast api up there cant work on its own i think
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)