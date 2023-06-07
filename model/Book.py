from datetime import date as date_type

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, func, text
from sqlalchemy.ext.declarative import declarative_base

try:
    from database import Base
except:
    Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    @classmethod
    def create_table(cls, engine):
        engine.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS book (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description VARCHAR(255),
                CONSTRAINT unique_title UNIQUE (title)
            );
            """
            )
        )


class BookDetails(Base):
    __tablename__ = "book_details"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    borrower_id = Column(Integer)
    borrower_email = Column(String)
    borrowed_date = Column(Date)
    borrowed_due_date = Column(Date)
    returned_date = Column(Date)
    returned = Column(Boolean)
    late = Column(Boolean)

    @classmethod
    def create_view(cls, engine):
        engine.execute(
            text(
                """
            DROP VIEW IF EXISTS book_details;
            CREATE VIEW book_details AS
            SELECT bk.id, bk.title, bk.description, u.id AS borrower_id, u.email AS borrower_email,
                    b.borrowed_date, b.borrowed_due_date, b.returned_date,
                    CASE
                        WHEN b.returned_date IS NOT NULL THEN
                            CASE
                                WHEN b.returned_date > b.borrowed_due_date THEN True
                                ELSE False
                            END
                        ELSE
                            CASE
                                WHEN CURDATE() > b.borrowed_due_date THEN True
                                ELSE False
                            END
                    END AS late
                FROM borrowing AS b
                LEFT JOIN userauth AS u ON b.user_id = u.id
                LEFT JOIN book AS bk ON b.book_id = bk.id;
        """
            )
        )


class BookModel(BaseModel):
    id: int
    title: str
    description: str


class BookModelDetail(BaseModel):
    id: int
    title: str
    description: str
    borrower_id: int
    borrower_email: str
    borrowed_date: date_type
    borrowed_due_date: date_type
    returned_date: date_type = None
    late: bool


class BookPost(BaseModel):
    title: str
    description: str


class BookPut(BaseModel):
    title: str = None
    description: str = None
