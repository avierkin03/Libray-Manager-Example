# скрипт crud.py для взаємодії з даними в базі

from sqlalchemy.orm import Session
from . import models, schemas


# Функція, яка повертає конкретного автора (по його id)
def read_author(db: Session, author_id: int):
    author_info = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author_info


# Функція, яка повертає всіх авторів
def read_authors(db: Session):
    authors = db.query(models.Author).offset(0).limit(300).all()
    return authors


# Функція, яка створює нового автора
def create_author(db: Session, new_author: schemas.AuthorClient):
    new_author_db = models.Author(name = new_author.name)
    # додавання екземпляру new_author_db до сеансу бази даних
    db.add(new_author_db)
    # фіксація змін в базі даних (щоб вони були збережені)
    db.commit()
    # оновлення екземпляру new_author_db (щоб він містив будь-які нові дані з бази даних)
    db.refresh(new_author_db)
    return new_author_db


# Функція, яка повертає всі книги
def read_books(db: Session):
    books = db.query(models.Book).offset(0).limit(300).all()
    return books


# Функція, яка створює нову книгу у конкретного автора
def create_author_book(db: Session, new_book: schemas.BookClient, author_id: int):
    book_db = models.Book(title = new_book.title, pages = new_book.pages, author_id = author_id)
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db


# Функція, яка видаляє книгу у конкретного автора
def delete_author_book(db: Session, title: str, author_id: int):
    book_db = db.query(models.Book).filter(models.Book.title == title, models.Book.author_id == author_id).first()

    if book_db is None:
        return {"повідомлення": "Такої книги не існує"}
    
    db.delete(book_db)
    db.commit()
    return {"повідомлення": "Книгу було успішно видалено"}