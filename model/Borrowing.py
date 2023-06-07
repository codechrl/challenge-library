from datetime import date as date_type

from pydantic import BaseModel
from sqlalchemy import Column, Date, ForeignKey, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

try:
    from database import Base
except:
    Base = declarative_base()


class Borrowing(Base):
    __tablename__ = "borrowing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("userauth.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    borrowed_date = Column(Date, nullable=False)
    borrowed_due_date = Column(Date, nullable=False)
    returned_date = Column(Date)

    user = relationship("UserAuth", backref="borrowing")
    book = relationship("Book", backref="borrowing")

    @classmethod
    def create_table(cls, engine):
        engine.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS `borrowing` (
            `id` int NOT NULL AUTO_INCREMENT,
            `user_id` int NOT NULL,
            `book_id` int NOT NULL,
            `borrowed_date` date NOT NULL,
            `borrowed_due_date` date NOT NULL,
            `returned_date` date DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `fk_user` (`user_id`),
            KEY `fk_book` (`book_id`),
            CONSTRAINT `fk_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
            CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`id`)
            )
            """
            )
        )


class BorrowingModel(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_date: date_type
    borrowed_due_date: date_type
    returned_date: date_type = None


class BorrowingPost(BaseModel):
    user_id: int
    book_id: int
    borrowed_date: date_type = None
    borrowed_due_date: date_type = None


class BorrowingPut(BaseModel):
    user_id: int = None
    book_id: int = None
    borrowed_date: date_type = None
    borrowed_due_date: date_type = None
    returned_date: date_type = None
