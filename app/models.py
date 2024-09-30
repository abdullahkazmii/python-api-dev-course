# type: ignore
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish = Column(Boolean, server_default="True" , nullable=False)
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    users_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    posts_id = Column(Integer, ForeignKey("Post.id", ondelete="CASCADE"), primary_key=True)

