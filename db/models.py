# Тут знаходяться класи, які будуть представляти собою моделі SQLAlchemy (Таблиці з БД)

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

# Клас автора
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key = True)
    name = Column(String, unique=True)
    books = relationship("Book", backref="parent")


# Клас книги
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True)
    title = Column(String, unique=True)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
