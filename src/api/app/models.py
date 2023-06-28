from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hash(password.encode('utf8'))

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    pages = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship('Author', back_populates='books')


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', back_populates='author')

    @property
    def num_books(self):
        return len(self.books)
