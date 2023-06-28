from sqlalchemy.orm import Session
from src.api.app.db import get_db
from src.api.app.models import User, Book, Author


# Seed function
def seed_data(db: Session):
    # Create test user
    user = User(username="admin_user", password="admin_password")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create test authors
    author1 = Author(name="Author 1")
    db.add(author1)
    db.commit()
    db.refresh(author1)

    author2 = Author(name="Author 2")
    db.add(author2)
    db.commit()
    db.refresh(author2)

    # Create test books
    book1 = Book(title="Book 1", pages=100, author_id=author1.id)
    db.add(book1)
    db.commit()
    db.refresh(book1)

    book2 = Book(title="Book 2", pages=200, author_id=author1.id)
    db.add(book2)
    db.commit()
    db.refresh(book2)

    book3 = Book(title="Book 3", pages=300, author_id=author2.id)
    db.add(book3)
    db.commit()
    db.refresh(book3)

# Seed the data
db = next(get_db())
seed_data(db)
