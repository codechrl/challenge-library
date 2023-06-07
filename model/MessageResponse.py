from typing import List, TypeVar, Union

from pydantic import BaseModel

from model.Book import BookModel, BookModelDetail
from model.Borrowing import BorrowingModel
from model.Userauth import Token

T = TypeVar("T")


class ValidationError(BaseModel):
    loc: list = None
    msg: str = None
    type: str = None


class BasicMessage(BaseModel):
    message: str


class IdMessage(BaseModel):
    id: int


class Pagination(BaseModel):
    page: int
    limit: int
    total_page: int = 0
    total_all: int = 0


class Response(BaseModel):
    status: str = "success"
    code: int = 200
    message: Union[dict, str, List[ValidationError]] = None
    data: Union[
        dict, List[T], IdMessage, BookModel, BookModelDetail, BorrowingModel, Token
    ] = None
    pagination: Pagination = None


class ValidationErrorResponse(Response):
    message: List[ValidationError] = None


class IdResponse(Response):
    data: IdMessage = None


class BookResponse(Response):
    data: List[BookModel] = None


class BookDetailResponse(Response):
    data: List[BookModelDetail] = None


class BorrowingResponse(Response):
    data: List[BorrowingModel] = None


class RegisterResponse(Response):
    data: dict = None


class LoginResponse(Response):
    data: Token = None
