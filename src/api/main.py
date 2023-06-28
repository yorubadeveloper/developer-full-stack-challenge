from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.app.db import Base, engine
from src.api.app.auth import router as auth_routes
from src.api.app.book import router as book_routes
from src.api.app.author import router as author_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(book_routes.router)
app.include_router(author_routes.router)

