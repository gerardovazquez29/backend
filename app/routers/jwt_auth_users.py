from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


## http://127.0.0.1:8000/jwtauth/login

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

router = APIRouter(
    prefix="/jwtauth",
    tags=["Jwtauth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

user_db = {
    "gerardo": {
        "username": "gerardo",
        "full_name": "gerardo vazquez",
        "email": "gerardo@vazquez.com",
        "disabled": False,
        "password": "$2a$12$rMinqqQkvpwplfGFYjP8peTVaKsLwIW3V6mQDKGCYay0MZnob.ZtC"
    },
    "santi": {
        "username": "santi",
        "full_name": "Santiago",
        "email": "santi@tovar.com",
        "disabled": True,
        "password": "$2a$12$UZGXpOtx9FptWMDR1H2fEundq.gHXLK5qRiPF2h5elESE/AK7SRCO"
    }
}

def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    
def search_user(username: str):
    if username in user_db:
        return User(**user_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion no validas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    print("[DEBUG] form.username:", form.username)
    print("[DEBUG] form.password:", form.password)
    user_data = user_db.get(form.username)
    print("[DEBUG] user_data:", user_data)
    if not user_data:
        print("[DEBUG] Usuario no encontrado en user_db")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    print("[DEBUG] user:", user)
    if user is None:
        print("[DEBUG] search_user_db devolvió None")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )

    try:
        password_check = crypt.verify(form.password, user.password)
        print("[DEBUG] password_check:", password_check)
    except Exception as e:
        print("[DEBUG] Error verificando contraseña:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verificando contraseña")

    if not password_check:
        print("[DEBUG] Contraseña incorrecta")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta")

    try:
        access_token ={"sub": user.username,
                        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}
        token = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)
        print("[DEBUG] access_token generado correctamente")
    except Exception as e:
        print("[DEBUG] Error generando access_token:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generando access_token")

    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

