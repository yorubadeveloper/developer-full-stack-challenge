from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.app import schemas
from src.api.app.db import get_db
from src.api.app.models import Author, User
from src.api.app.helper import get_current_user

router = APIRouter(prefix="/author", tags=["Author"])


# Author routes
@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_author = Author(name=author.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=schemas.Author)
def edit_author(author_id: int, author: schemas.AuthorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    author_db = db.query(Author).filter(Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    author_db.name = author.name
    db.commit()
    db.refresh(author_db)
    return author_db


@router.get("/all/", response_model=schemas.AuthorsResponse)
def get_all_author(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return {"authors": authors}
