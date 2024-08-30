import base64
import datetime
import json
import random

from sqlalchemy import create_engine, select, inspect, insert, update, delete, desc, asc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only

from app.core.config import settings


Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.DB_URL, echo=False, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            return conn

    @staticmethod
    def create_all_tables(bind):
        Base.metadata.create_all(bind)

    async def execute(self, query, params=None):
        async with self.async_session() as session:
            async with session.begin():
                if params:
                    result = await session.execute(query, params)
                else:
                    result = await session.execute(query)
                data = result.all()
                return [row._mapping for row in data]

    async def execute_many(self, query, params_list):
        async with self.async_session() as session:
            async with session.begin():
                results = []
                for params in params_list:
                    result = await session.execute(query, params)
                    data = result.all()
                    results.append([row._mapping for row in data])
                return results

    async def insert(self, table, data):
        stmt = insert(table).values(data)
        async with self.engine.connect() as connection:
            result = await connection.execute(stmt)
            await connection.commit()
            return result.inserted_primary_key[0]

    async def add(self, model):
        async with self.engine.connect() as connection:
            async with self.async_session() as session:
                async with session.begin():
                    session.add(model)
            await connection.commit()

    async def commit(self):
        async with self.engine.connect() as connection:
            await connection.commit()

    async def update(self, table, data, where=None):
        stmt = update(table)
        if where:
            stmt = stmt.where(*where)
        stmt = stmt.values(data)
        async with self.engine.connect() as connection:
            result = await connection.execute(stmt)
            await connection.commit()
            return result.rowcount

    async def delete(self, table, where):
        stmt = delete(table).where(*where)
        async with self.engine.connect() as connection:
            result = await connection.execute(stmt)
            await connection.commit()
            return result.rowcount

    async def close(self):
        await self.engine.dispose()

    async def get_data(self, table, where=None, values=None, return_list=False, group_by=None, fetchall=True,
                       limit: int or None = 100,
                       order_by=None, join=None, subquery=None, outerjoin=None, load_only_=None, offset=None,
                       convert_list=None) -> object or None:
        if values is not None:
            if isinstance(values, (list, tuple)):
                query = select(*values).select_from(table)
            else:
                query = select(values).select_from(table)
        else:
            query = select(table)
        if load_only_ is not None:
            if isinstance(load_only_, (list, tuple)):
                query = query.options(load_only(*load_only_))
            else:
                query = query.options(load_only(load_only_))
        if where:
            query = query.where(*where)
        if group_by is not None:
            query = query.group_by(group_by)
        if order_by is not None:
            query = query.order_by(order_by)
        if join is not None:
            if isinstance(join, (list, tuple)):
                query = query.join(*join)
            else:
                query = query.join(join)
        if outerjoin is not None:
            if isinstance(outerjoin, (list, tuple)):
                query = query.outerjoin(*outerjoin)
            else:
                query = query.outerjoin(outerjoin)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if subquery:
            query = query.subquery()
            return query
        async with (self.async_session() as session):
            result = await session.execute(query)
            if fetchall:
                if return_list:
                    data = result.fetchall()
                    if convert_list:
                        data = list(list(x) for x in data)
                else:
                    data = result.scalars()
                    if data:
                        data = data.all()
                return data
            else:
                data = result.scalar()

                return data


async def get_db() -> Database:
    db: Database = Database()
    try:
        yield db
    finally:
        await db.close()
