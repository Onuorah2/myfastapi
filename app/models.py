from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP   

class Post(Base):
    __tablename__ =  'posts'

    id = Column(Integer, primary_key= True, nullable= False )  #nullable means that if it can be null
    title = Column(String, nullable = False)
    content = Column(String, nullable= False)
    publish = Column(String, server_default= 'true', nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default= text('now()') )
    owner_id = Column(Integer, ForeignKey('users.id', ondelete= 'CASCADE'), nullable=False) #linking this to the users. users.id(users is the name od the other table and id is what we are making a referwnce too. whats we are referencing here is the __table__ name and not the class name(User))

    owner = relationship('User')   #this will form a relationship between the post and the user so thst when we retrieve a post,  it will return a owner property(username or email). it will just fetch the user based of the owner id and display the username.we are refrencing the class name and not the table name

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True) #unique means, no other user should have the same email
    password = Column(String, nullable=False)
 #   created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key= True)

