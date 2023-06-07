from sqlalchemy import Table

from database import db
from model.Book import Book, BookDetails
from model.Borrowing import Borrowing
from model.Userauth import Userauth
from route.userauth import get_password_hash


async def post_db(table_name, data: dict):
    try:
        database = db.get_database()
        table = Table(table_name, db.get_metadata(), autoload_with=db.get_engine())

        query = table.insert().values(data)
        await database.execute(query)

    except Exception as exc:
        print(str(exc))


users = [
    {"email": "john@gmail.com", "password": get_password_hash("Abcdefg1")},
    {"email": "alice@example.com", "password": get_password_hash("pass123")},
    {"email": "emma@yahoo.com", "password": get_password_hash("123pass")},
    {"email": "michael@hotmail.com", "password": get_password_hash("heYtay01")},
    {"email": "sarah@example.co.id", "password": get_password_hash("1234567B")},
]

books = [
    {"title": "The Great Gatsby", "description": "A novel by F. Scott Fitzgerald"},
    {"title": "To Kill a Mockingbird", "description": "A novel by Harper Lee"},
    {"title": "1984", "description": "A dystopian novel by George Orwell"},
    {"title": "Pride and Prejudice", "description": "A novel by Jane Austen"},
    {"title": "The Catcher in the Rye", "description": "A novel by J.D. Salinger"},
]
borrowings = [
    {
        "id": 1,
        "user_id": 1,
        "book_id": 1,
        "borrowed_date": "2023-05-01",
        "borrowed_due_date": "2023-05-15",
        "returned_date": None,
    },
    {
        "id": 2,
        "user_id": 2,
        "book_id": 3,
        "borrowed_date": "2023-05-02",
        "borrowed_due_date": "2023-05-16",
        "returned_date": "2023-05-14",
    },
    {
        "id": 3,
        "user_id": 3,
        "book_id": 2,
        "borrowed_date": "2023-05-03",
        "borrowed_due_date": "2023-05-17",
        "returned_date": "2023-05-16",
    },
    {
        "id": 4,
        "user_id": 4,
        "book_id": 4,
        "borrowed_date": "2023-05-04",
        "borrowed_due_date": "2023-05-18",
        "returned_date": "2023-05-20",
    },
    {
        "id": 5,
        "user_id": 5,
        "book_id": 5,
        "borrowed_date": "2023-05-05",
        "borrowed_due_date": "2023-05-19",
        "returned_date": None,
    },
]


async def run_seeds():
    try:
        print("INFO:", "    Running Migrations")
        engine = db.get_engine()
        Userauth.create_table(engine=engine)
        Book.create_table(engine=engine)
        Borrowing.create_table(engine=engine)
        BookDetails.create_view(engine=engine)

        print("INFO:", "    Seeding Database")
        for row in users:
            await post_db("userauth", row)

        for row in books:
            await post_db("book", row)

        for row in borrowings:
            await post_db("borrowing", row)

        print("INFO:", "    Migrations Finished")
        return True

    except Exception as exc:
        print(str(exc))
        return False
