from typing import Dict
from uuid import uuid1

from model import Book, User


class BookDatabase:
    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}

    def add_book(self, name: str, author: str) -> None:
        if name in self.books:
            raise ValueError("Book already exists")

        book = Book(id=uuid1(), title=name, author=author)
        self.books[book.title] = book

    def get_book(self, name: str) -> Book:
        if name not in self.books:
            raise ValueError("Book not found")

        return self.books[name]

    def delete_book(self, name: str) -> None:
        if name not in self.books:
            raise ValueError("Book not found")

        del self.books[name]

    def list_books(self) -> Dict[str, Book]:
        return self.books


class UserDatabase:
    def __init__(self) -> None:
        self.users: Dict[str, User] = {}

    def add_user(self, username: str, password: str) -> None:
        if username in self.users:
            raise ValueError("User already exists")

        user = User(id=uuid1(), username=username, password=password)
        self.users[user.username] = user

    def get_user(self, username: str) -> User:
        if username not in self.users:
            raise ValueError("User not found")

        return self.users[username]

    def delete_user(self, username: str) -> None:
        if username not in self.users:
            raise ValueError("User not found")

        del self.users[username]

    def list_users(self) -> Dict[str, User]:
        return self.users


book_db = BookDatabase()
user_db = UserDatabase()


def get_book_db() -> BookDatabase:
    if not book_db:
        raise ValueError("Database connection error")

    return book_db


def get_user_db() -> UserDatabase:
    if not user_db:
        raise ValueError("Database connection error")

    return user_db
