import inspect

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import Table, func

from database import db
from model.Book import BookPost, BookPut
from model.MessageResponse import BookDetailResponse, BookResponse, Response

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def get_book(
    id: int = None,
    title: str = None,
    desc: str = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    asc: bool = True,
):
    try:
        database = db.get_database()
        table = Table("book", db.get_metadata(), autoload_with=db.get_engine())

        query = table.select()
        if id:
            query = query.where(table.c.id == id)
        if title:
            query = query.filter(table.c.title.ilike(f"%{title.lower()}%"))
        if desc:
            query = query.filter(table.c.description.ilike(f"%{desc.lower()}%"))

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

        return BookResponse(
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


@router.get("/details", status_code=status.HTTP_200_OK)
async def get_book_details(
    id: int = None,
    title: str = None,
    desc: str = None,
    returned: bool = None,
    late: bool = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    asc: bool = True,
):
    try:
        database = db.get_database()
        table = Table("book_details", db.get_metadata(), autoload_with=db.get_engine())

        query = table.select().with_only_columns(
            table.c.id,
            table.c.title,
            table.c.description,
            table.c.borrower_id,
            table.c.borrower_email,
            table.c.borrowed_date,
            table.c.borrowed_due_date,
            table.c.returned_date,
            table.c.late,
        )
        if id:
            query = query.where(table.c.id == id)
        if title:
            query = query.filter(table.c.title.ilike(f"%{title.lower()}%"))
        if desc:
            query = query.filter(table.c.description.ilike(f"%{desc.lower()}%"))
        if returned is False:
            query = query.where(table.c.returned_date is None)
        else:
            query = query.where(table.c.returned_date is not None)
        if late is False:
            query = query.where(table.c.late is False)
        else:
            query = query.where(table.c.late is True)

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

        return BookDetailResponse(
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
async def post_book(data: BookPost):
    try:
        database = db.get_database()
        table = Table("book", db.get_metadata(), autoload_with=db.get_engine())

        query = table.insert().values(data.dict())

        returning_id = await database.execute(query)
        return Response(
            status="success",
            code=201,
            message={"id": returning_id},
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def put_book(id: int, data: BookPut):
    try:
        database = db.get_database()
        table = Table("book", db.get_metadata(), autoload_with=db.get_engine())

        data_dict = data.dict()
        data_dict = {
            key: value for key, value in data_dict.items() if value is not None
        }

        query = table.update().where(table.c.id == id).values(data_dict)

        await database.execute(query)
        return Response(
            status="success",
            code=200,
            message={"id": id},
            data=data_dict,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def delete_book(id: int):
    try:
        database = db.get_database()
        table = Table("book", db.get_metadata(), autoload_with=db.get_engine())

        query = table.delete().where(table.c.id == id)

        await database.execute(query)
        return Response(
            status="success",
            code=200,
            message={"id": id},
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
