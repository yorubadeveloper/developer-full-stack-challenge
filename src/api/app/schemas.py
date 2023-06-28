from typing import List
from pydantic import BaseModel
import datetime


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str


class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDB(User):
    password: str


# Book schema
class BookBase(BaseModel):
    title: str
    pages: int


class BookCreate(BookBase):
    author_id: int


class BookEdit(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


# Author schema
class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    num_books: int
    books: List[Book]

    class Config:
        orm_mode = True


class AuthorsResponse(BaseModel):
    authors: List[Author]


class AuthorResponse(AuthorBase):
    id: int
    num_books: int

    class Config:
        orm_mode = True


class BookResponse(BookBase):
    id: int
    author_id: int
    author: AuthorResponse

    class Config:
        orm_mode = True


class Books(BaseModel):
    books: List[BookResponse]
