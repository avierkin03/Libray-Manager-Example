from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker                 # допомагає керувати сесіями бази даних

# URL-адресa для бази даних 
# (підключення до бази даних SQLite (файл із базою даних SQLite). Файл буде розташовано в тому самому каталозі)
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# створюємо engine - точка входу до бази даних(передаємо шлях для БД, а також налаштування для SQLite)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

# створюємо екземпляр класу SessionLocal, який буде фактичним сеансом бази даних (для кожного запиту буде створюватися окрема сесія)
# Сесія - це проміжний шар між Python-кодом і БД. Вона використовується для додавання, зчитування, оновлення та видалення об'єктів у БД.
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# створюємо клас Вase, який знадобиться пізніше, щоб створити кожну з моделей бази даних
Base = declarative_base()