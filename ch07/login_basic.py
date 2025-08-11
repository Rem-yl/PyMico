"""
uvicorn login_basic:app --reload

curl -X POST "http://127.0.0.1:8000/signup?username=rem&password=123"
curl -u rem:123 "http://127.0.0.1:8000/login

"""

from database import Base, SessionFactory, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Basic Auth
security = HTTPBasic()

app = FastAPI()

# 用户表


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


# 创建新用户（注册）
@app.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    # 检查是否已存在
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    hashed_pw = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}


# 登录验证


@app.get("/login")
def login(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"message": f"欢迎你，{credentials.username}"}
