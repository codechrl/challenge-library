import inspect
import re
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import Table, func

from database import db
from model.Borrowing import BorrowingPost
from model.MessageResponse import BorrowingResponse


def validate_email(email):
    pattern = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(pattern, email):
        return True
    else:
        return False


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8}$"
    if re.match(pattern, password):
        return True
    else:
        return False


async def validate_borrowing_user(user_id):
    database = db.get_database()
    table = Table("borrowing", db.get_metadata(), autoload_with=db.get_engine())

    query = (
        table.select()
        .with_only_columns(table.c.user_id)
        .where(table.c.user_id == user_id, table.c.returned_date == None)
    )

    data = await database.fetch_all(query)

    if len(data) == 0:
        return True
    else:
        return False
