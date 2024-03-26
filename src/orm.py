import asyncio
from dataclasses import dataclass

from sqlalchemy import select, desc, asc

from settings import settings
from database import Database
from models import LocationsOrm
from exceptions import NotFoundException


class AsyncOrm:
    __database_instance = Database(settings.DATABASE_URL_asyncpg)

    async def create_database(self):
        await self.__database_instance.create_database()

    async def insert_location_data(self, data: dataclass):
        dict_data = data.__dict__

        async with self.__database_instance.session() as session:
            new_location = LocationsOrm(**dict_data)

            session.add(new_location)
            await session.commit()

    async def select_all_locations(self) -> list:
        list_of_locations = []
        async with self.__database_instance.session() as session:
            locations = select(LocationsOrm)
            result = await session.execute(locations)
            rows = result.fetchall()

            for row in rows:
                location_dict = row[0].as_dict()
                list_of_locations.append(location_dict)

        if list_of_locations:
            return list_of_locations
        else:
            raise NotFoundException("No locations found.")

    async def select_the_most_populated_location(self) -> list:
        async with self.__database_instance.session() as session:
            locations = select(LocationsOrm) \
                .filter(LocationsOrm.location != "World")\
                .order_by(desc(LocationsOrm.population)) \
                .limit(1)

            result = await session.execute(locations)
            row = result.fetchone()

            if row is not None:
                location_dict = row[0].as_dict()
                return [location_dict]
            else:
                raise NotFoundException("No locations found.")

    async def select_the_less_populated_location(self):
        async with self.__database_instance.session() as session:
            locations = select(LocationsOrm) \
                .order_by(asc(LocationsOrm.population)) \
                .limit(1)

            result = await session.execute(locations)
            row = result.fetchone()

            if row is not None:
                location_dict = row[0].as_dict()
                return [location_dict]
            else:
                raise NotFoundException("No locations found.")


async def main():
    orm = AsyncOrm()
    await orm.create_database()


if __name__ == '__main__':
    asyncio.run(main())
