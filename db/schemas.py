# Тут знаходяться класи, які будуть представляти собою Pydantic моделі

from typing import Union
from pydantic import BaseModel, Field

# Модель для валідації книг, отриманих від користувача
class BookClient(BaseModel):
    title: str
    pages: int

# Модель для валідації книг, отриманих з бази даних (ми вже знатимемо id та author_id)
class BookDB(BookClient):
    id: int
    author_id: int
    class Config:
        from_attributes = True

# Модель для валідації авторів, отриманих від користувача
class AuthorClient(BaseModel):
    name: str

# Модель для валідації авторів, отриманих з бази даних (ми вже знатимемо id та books)
class AuthorDB(AuthorClient):
    id: int
    books: list[BookDB] = []
    class Config:
        from_attributes = True