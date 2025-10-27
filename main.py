from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import crud, models, schemas
from db.database import SessionLocal, engine

# створюємо таблиці в базі даних, якщо вони ще не існують
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# Монтування статичних файлів і шаблонів
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Залежність
# Її суть: створювати сесію для кожного запиту, а коли запит закінчується то закривати її 
def get_db():
    # створюємо об'єкт-сесію SQLAlchemy
    db = SessionLocal()
    try:
        # віддає сесію коду, що її потребує (наприклад, роуту)
        yield db
    finally:
        # закриває з’єднання після завершення запиту
        db.close()


# Маршрут для сторінки входу
@app.get("/", response_class=HTMLResponse)
def start_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("authors.html", {"request": request, "authors": crud.read_authors(db)})


# Сторінка створення автора
@app.get("/create_author/", response_class=HTMLResponse)
def create_author_page(request: Request):
    return templates.TemplateResponse("create_author.html", {"request": request})

# маршрут для створення нового автора
@app.post("/authors/", response_class=HTMLResponse)
def create_author(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    author = schemas.AuthorClient(name=name)
    crud.create_author(db, author)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": crud.read_authors(db)})


# маршрут для створення нового автора
@app.post("/authors/", response_model = schemas.AuthorDB)
#db: Session = Depends(get_db) - FastAPI автоматично викликає get_db() і передає в db готову сесію БД
def create_author(author: schemas.AuthorClient, db: Session = Depends(get_db)):
    return crud.create_author(db = db, new_author = author)


# маршрут для отримання всіх авторів
@app.get("/authors/", response_class=HTMLResponse)
def read_authors(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("authors.html", {"request": request, "authors": crud.read_authors(db)})


# маршрут для отримання конкретного автора по його id
@app.get("/authors/{author_id}", response_model = schemas.AuthorDB)
def read_authors(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.read_author(db, author_id = author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return db_author


# Сторінка створення книги 
@app.get("/create_book/{author_id}", response_class=HTMLResponse)
def create_book_page(request: Request, author_id: int):
    return templates.TemplateResponse("create_book.html", {"request": request, "author_id": author_id})


# маршрут для створення книг для конкретного автора
@app.post("/authors/{author_id}/books/", response_class=HTMLResponse)
def create_book_for_author(
    request: Request,
    author_id: int,
    title: str = Form(...),
    pages: int = Form(...),
    db: Session = Depends(get_db)
):
    book = schemas.BookClient(title=title, pages=pages)
    crud.create_author_book(db=db, new_book=book, author_id=author_id)
    return templates.TemplateResponse("books.html", {"request": request, "books": crud.read_books(db)})


# маршрут для отримання всіх книг
@app.get("/books/", response_class=HTMLResponse)
def read_books(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("books.html", {"request": request, "books": crud.read_books(db)})


# маршрут для видалення книги для конкретного автора
@app.post("/delete_book/{author_id}/{title}", response_class=HTMLResponse)
def delete_book(request: Request, author_id: int, title: str, db: Session = Depends(get_db)):
    crud.delete_author_book(db=db, title=title, author_id=author_id)
    return templates.TemplateResponse("books.html", {"request": request, "books": crud.read_books(db)})