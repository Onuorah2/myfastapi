from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = postgres://myapi_4jxf_user:uwRA2kJKk9AQCBT3NuDx86Q0lK4xTvV2@dpg-choqm6m7avjb90itejgg-a/myapi_4jxf
engine = create_engine(SQLALCHEMY_DATABASE_URL)#this is the engine responsible for establishing a aconnection to talk with the database. to connect with the database and then you pass in the connection string

Sessionlocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)#when you want to talk with the database, u have to make use of a session

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
