import inspect
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import Table, func

from database import db
from model.Borrowing import BorrowingPost, BorrowingPut
from model.MessageResponse import BookResponse, BorrowingResponse, Response
from util.validation import validate_borrowing_user

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=BorrowingResponse)
async def get_borrowing(
    id: int = None,
    user_id: int = None,
    book_id: int = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    asc: bool = True,
):
    try:
        database = db.get_database()
        table = Table("borrowing", db.get_metadata(), autoload_with=db.get_engine())

        query = query = table.select()
        if id:
            query = query.where(table.c.id == id)
        if user_id:
            query = query.where(table.c.user_id == user_id)
        if book_id:
            query = query.where(table.c.book_id == book_id)

        total_count = await database.fetch_val(
            query.with_only_columns(func.count(table.c.id).label("count"))
        )
        query = query.limit(limit).offset(limit * (page - 1))

        if asc:
            query = query.order_by(table.c[order_by].asc())
        else:
            query = query.order_by(table.c[order_by].desc())

        data_result = await database.fetch_all(query)

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        args = {arg: values[arg] for arg in args if values[arg]}

        return BorrowingResponse(
            status="success",
            code=200,
            message=args,
            data=data_result,
            pagination={
                "total_all": total_count,
                "total_page": len(data_result),
                "page": page,
                "limit": limit,
            },
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def post_borrowing(data: BorrowingPost):
    if not await validate_borrowing_user(data.user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is currently borrowing a book.",
        )

    try:
        current_date = datetime.now().date()
        if not data.borrowed_date:
            data.borrowed_date = current_date
        if not data.borrowed_due_date:
            data.borrowed_due_date = data.borrowed_date + timedelta(days=3)

        database = db.get_database()
        table = Table("borrowing", db.get_metadata(), autoload_with=db.get_engine())

        query = table.insert().values(
            user_id=data.user_id,
            book_id=data.book_id,
            borrowed_date=data.borrowed_date,
            borrowed_due_date=data.borrowed_due_date,
        )

        return_id = await database.execute(query)
        return Response(
            status="success",
            code=201,
            message={"id": return_id},
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def post_borrowing(id: int, data: BorrowingPut):
    # if not await validate_borrowing_user(data.user_id):
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="User is currently borrowing a book.",
    #     )

    try:
        database = db.get_database()
        table = Table("borrowing", db.get_metadata(), autoload_with=db.get_engine())

        data_dict = data.dict()
        data_dict = {
            key: value for key, value in data_dict.items() if value is not None
        }

        query = table.update().where(table.c.id == id).values(data_dict)

        return_id = await database.execute(query)
        return Response(
            status="success",
            code=200,
            message={"id": id},
            data=data_dict,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def post_borrowing(id: int):
    try:
        database = db.get_database()
        table = Table("borrowing", db.get_metadata(), autoload_with=db.get_engine())

        query = table.delete().where(table.c.id == id)

        return_id = await database.execute(query)
        return Response(
            status="success",
            code=200,
            message={"id": id},
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
