from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.database import schemas
from app.database.session import get_db
from app.cruds import auth_crud
from app.core import security


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_crud.create_user(db, user_in)


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    user = auth_crud.authenticate_user(
        db, form_data.username, form_data.password)
    data = {"sub": str(user.id)}
    access_token = security.create_access_token(data)
    refresh_token = security.create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = security.decode_token(refresh_token)
    if not payload or payload.get("scope") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    data = {"sub": str(user_id)}
    access_token = security.create_access_token(data)
    new_refresh = security.create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.UserOut)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.decode_token(token)
    user = auth_crud.get_user_by_id(db, int(payload.get("sub")))
    return user
