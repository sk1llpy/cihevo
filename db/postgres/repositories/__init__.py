from typing import Any
from abc import abstractmethod, ABC
from sqlalchemy import select, and_, select, insert, delete, update, and_, desc, asc
from sqlalchemy.exc import IntegrityError
import os
from conf.components import MEDIA_ROOT
from sqlalchemy.orm import Session, Query
from sqlalchemy.ext.asyncio import AsyncSession
from API.exceptions import order_by_field_not_found, integrity_error
from db.postgres.handlers import commit_async_session


class BaseRepository(ABC):
    table = None

    def __init__(self, session: Session | AsyncSession = None) -> None:
        self.session: Session | AsyncSession = session

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_many(self):
        pass

    @abstractmethod
    def exists(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class AsyncRepository(BaseRepository):
    table = None

    def __init__(
            self, session: AsyncSession = None,
            limit: int = 10, offset: int = 1,
            order_by: list[str] = ['-created_at'],
            commit_mode: bool = True) -> None:
        self.session = session
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.commit_mode = commit_mode

    async def desc_or_asc(self, field_name: str):
        try:
            if field_name[0] == "-":
                return desc, field_name.replace('-', '')
        except IndexError:
            raise
        return asc, field_name
    
    async def get_attribute(self, field_name: str):
        try:
            return getattr(self.table, field_name)
        except AttributeError:
            raise order_by_field_not_found
        
    async def order(self, query: Query):
        order_by = list()
        for field_name in self.order_by:
            operator, field_name = await self.desc_or_asc(field_name)
            table_field = await self.get_attribute(field_name)
            order_by.append(operator(table_field))

        if not self.order_by:
            order_by = [desc(self.table.created_at)]

        return query.order_by(*order_by)
    async def paginate(self, query: Query):
        return query.limit(self.limit).offset(self.offset)

    async def select_actives(self, conditions: dict):
        conditions.update({
            'is_active': True
        })
        return conditions

    async def generate_where(self, conditions: dict, all: bool = False):
        if not all:
            conditions = await self.select_actives(conditions)
        return and_(*[getattr(self.table, field) == value for field, value in conditions.items()])

    async def searching_where(self, conditions: dict):
        #conditions = await self.select_actives(conditions)
        return and_(*[getattr(self.table, field).ilike(f"%{value}%") for field, value in conditions.items()])

    async def schoose_attributes(self, attributes: list[str]):
        return [getattr(self.table, field)
                for field in attributes] if attributes else self.table

    async def generate_query(self, conditions: dict, attributes: dict = None) -> table:
        where_condition = await self.generate_where(conditions)
        attributes: [self.table] = await self.schoose_attributes(attributes)
        return select(attributes).where(where_condition)

    async def get(self, conditions: dict):
        """
        SELECT from self.table by specified attribute. Return one object
        """
        query = await self.generate_query(conditions=conditions)
        instance = (await self.execute(query)).scalar()
        return instance

    async def get_many(self, conditions: dict):
        """
        SELECT from self.table by specified attribute. Return many objects
        """
        query = await self.generate_query(conditions=conditions)
        instances = (await self.execute(query)).scalars().all()
        return instances

    async def exists(self, conditions: dict, attributes: dict = None) -> table:
        query = await self.generate_query(attributes=attributes, conditions=conditions)
        instance = (await self.execute(query)).scalar()
        return bool(instance)

    async def update(self, conditions, values: dict, all: bool = False):
        """
        Edit object with passed params
        """
        where_condition = await self.generate_where(conditions=conditions, all=all)
        query = update(self.table).where(where_condition).values(values)
        return await self.execute_and_commit(query=query)

    async def create(self, params: dict):
        """
        INSERT record
        """
        instance = self.table(**params)
        if self.commit_mode is True:
            self.session.add(instance)
            instance = await commit_async_session(session=self.session)
        print(instance)
        return instance

    async def delete(self, conditions: dict):
        where_condition = await self.generate_where(conditions=conditions)
        query = update(self.table).where(where_condition).values({
            'is_active': False
        })
        instance = await self.execute_and_commit(query=query)
        return instance

    async def execute(self, query: Query):
        async with self.session:
            try:
                instance = await self.session.execute(query)
            except IntegrityError:
                raise integrity_error
        return instance

    async def execute_and_commit(self, query: Query):
        async with self.session:
            try:
                instance = await self.session.execute(query)
            except IntegrityError:
                raise integrity_error
            if self.commit_mode is True:
                await commit_async_session(session=self.session)
        return instance

    async def create_dir(self, instance, filename, directory_name: str = None):
        # this is neseccary for django admin as it adds media dir itself so to save
        # we should pass just the path after media
        table: str = self.table.__tablename__
        file_dir_for_django = f"{table}/{directory_name}/{instance.id}/"
        if not directory_name:
            file_dir_for_django = f"{table}/{instance.id}/"
        file_directory = f"{MEDIA_ROOT}/{file_dir_for_django}/"
        try:
            os.makedirs(file_directory)
            file_full_path = file_directory + filename
        except FileExistsError:
            file_full_path = file_directory + filename

        return {
            'file_dir': file_dir_for_django,
            'file_full_path': file_full_path}

    async def create_conditions(self, conditions: dict):
        return and_(*[getattr(self.table, field) == value for field, value in conditions.items()])

class SyncRepository(BaseRepository):
    table = None

    def get(self, attribute: str, value: Any):
        """
        SELECT from self.table by specified attribute. Return one object
        """
        with self.session:
            instance = (self.session.execute(
                select(self.table).where(getattr(self.table, attribute) == value)
            )).scalar()

        return instance

    def get_many(self, attribute: str, value: Any):
        """
        SELECT from self.table by specified attribute. Return many objects
        """
        with self.session:
            instances = (self.session.execute(
                select(self.table).where(getattr(self.table, attribute) == value)
            )).scalars()

        return instances

    def exists(self, attribute: str, value: Any):
        with self.session:
            instance = (self.session.execute(
                select(getattr(self.table, attribute)).where(
                    getattr(self.table, attribute) == value))).scalar()

            return bool(instance)

    def update(self, conditions: dict, edits: dict):
        """
        Edit object with passed params
        """
        with self.session:
            where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
            stmt = update(self.table).where(where_condition).values(**edits)
            self.session.execute(stmt)
            self.session.commit()
        return None

    def create(self, params: dict):
        """
        INSERT record
        """
        with self.session:
            stmt = insert(self.table).values(**params)
            result = self.session.execute(stmt)
            self.session.commit()
        return result.fetchone()

    def delete(self, conditions: dict):
        try:
            where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
        except AttributeError:
            return None
        with self.session:
            stmt = delete(self.table).where(where_condition)
            self.session.execute(stmt)
            self.session.commit()

    def get_or_create(self, conditions: dict, params: dict):
        try:
            self.create(params=params)
        except IntegrityError:
            with self.session:
                where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
                result = self.session.query(self.table).filter(where_condition).scalar()
                return result

    def get_and_update(self, conditions: dict, edits: dict):
        with self.session:
            where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
            try:
                instance = (self.session.execute(select(self.table).where(where_condition))).scalar()
                for key, value in edits.items():
                    setattr(instance, key, value)
                self.session.add(instance)
                self.session.commit()
            except:
                return None
            return instance

    def execute(self, query: Query):
        with self.session:
            try:
                instance = self.session.execute(query)
            except IntegrityError:
                raise integrity_error
        return instance