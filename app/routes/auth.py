from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas import UserCreate, UserLogin
from app.models import User
from app.database import get_db
from app.auth_utils import verify_password, get_password_hash, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print("Received User:", user)  # ログを追加
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "アカウントが作成されました"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=timedelta(minutes=30))
    return {"token": access_token}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.auth_utils import decode_access_token
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
