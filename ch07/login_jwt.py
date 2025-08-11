from datetime import datetime, timedelta

# ===================== 数据库配置 =====================
from database import Base, SessionFactory, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# ===================== JWT 配置 =====================
SECRET_KEY = "cccccbihngtbhughfeidvkjdkrrikvfbefevkkuejcvg"  # 生产环境要放到环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 协议入口
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ===================== 数据模型 =====================


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))


Base.metadata.create_all(bind=engine)

# ===================== 工具函数 =====================


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ===================== API =====================
app = FastAPI()


@app.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = User(username=username, hashed_password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"欢迎你，{current_user.username}"}
