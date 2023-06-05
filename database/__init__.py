import asyncpg
import databases
import sqlalchemy
from settings import settings


class Pool:
    async def open_pool(self):
        self.database = databases.Database(settings.DBSTRING)
        self.metadata = sqlalchemy.MetaData()
        self.engine = sqlalchemy.create_engine(
            settings.DBSTRING, pool_size=1, max_overflow=0
        )
        self.metadata.create_all(self.engine)
        await self.database.connect()
        print("INFO:", "    Connected to database")

    async def close_pool(self):
        await self.database.disconnect()

    async def terminate_pool(self):
        await self.pool.terminate()

    def get_pool(self):
        return self.pool

    def get_database(self):
        return self.database

    def get_metadata(self):
        return self.metadata

    def get_engine(self):
        return self.engine


db = Pool()
