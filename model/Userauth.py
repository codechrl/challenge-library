from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

try:
    from database import Base
except:
    Base = declarative_base()


class Userauth(Base):
    __tablename__ = "userauth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @classmethod
    def create_table(cls, engine):
        engine.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS userauth (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
            );
        """
            )
        )


class UserIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expired_in: str
    user_profile: dict = None
