from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pymysql.err import IntegrityError
from sqlalchemy import Table

from database import db
from model.MessageResponse import RegisterResponse
from model.Userauth import Token
from setting import settings
from util.validation import validate_email, validate_password

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="userauth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_jwt

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse
)
async def register(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    # token: str = Depends(oauth2_scheme),
):
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email Format")

    if not validate_password(password):
        raise HTTPException(status_code=400, detail="Invalid Password Format")

    try:
        database = db.get_database()
        table = Table("userauth", db.get_metadata(), autoload_with=db.get_engine())

        hashed_password = get_password_hash(password)

        query = table.insert().values(email=email, password=hashed_password)
        await database.execute(query)

        return RegisterResponse(status="success", code=201, data={"email": email})

    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email Already Registered")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        database = db.get_database()
        table = Table("userauth", db.get_metadata(), autoload_with=db.get_engine())

        username = form_data.username
        password = form_data.password

        query = table.select().where(table.c.email == username)
        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        stored_password = result["password"]
        if not verify_password(password, stored_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        data = {"sub": username}
        token = create_jwt_token(data)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expired_in": ACCESS_TOKEN_EXPIRE_MINUTES,
            "user_profile": {"email": username},
        }

    except IntegrityError:
        raise HTTPException(status_code=409, detail="User or Book not exist.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/protected", status_code=status.HTTP_200_OK)
async def protected(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    email = payload.get("sub")

    print(payload)

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"email": email}
