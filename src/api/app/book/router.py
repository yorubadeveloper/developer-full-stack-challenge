from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.app import schemas
from src.api.app.db import get_db
from src.api.app.models import Book, User, Author
from src.api.app.helper import get_current_user

router = APIRouter(prefix="/book", tags=["Book"])


# Book routes
@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(title=book.title, pages=book.pages, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def edit_book(book_id: int, book: schemas.BookEdit, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.pages = book.pages
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def edit_book(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.refresh(db_book)
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.get("/all/", response_model=schemas.Books)
def get_all_book(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": books}

# Add more book routes as needed
