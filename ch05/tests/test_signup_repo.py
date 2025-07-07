from database import DATABASE_URL, Base
from models.login import Signup
from repo.signup import SignupRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
repo = SignupRepository(session)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def test_insert() -> None:
    signup = Signup(username="testuser", password="testpass")
    assert repo.insert_signup(signup) is True


def test_get_all() -> None:
    total_signup = repo.get_all()
    print(total_signup)


if __name__ == "__main__":
    init_db()
    test_insert()
    test_get_all()
