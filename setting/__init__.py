from pydantic import BaseSettings


class Settings(BaseSettings):
    DBSTRING: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
