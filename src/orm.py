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
                .order_by(desc(LocationsOrm.population_in_2023)) \
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
                .order_by(asc(LocationsOrm.population_in_2023)) \
                .limit(1)

            result = await session.execute(locations)
            row = result.fetchone()

            if row is not None:
                location_dict = row[0].as_dict()
                return [location_dict]
            else:
                raise NotFoundException("No locations found.")

    async def get_extreme_locations(self, region_name):
        async with self.__database_instance.session() as session:
            the_most_populated_location_query = (
                select(LocationsOrm)
                .filter(LocationsOrm.region == region_name)
                .order_by(LocationsOrm.population_in_2023.desc())
                .limit(1)
            )

            the_less_populated_location_query = (
                select(LocationsOrm)
                .filter(LocationsOrm.region == region_name)
                .order_by(LocationsOrm.population_in_2023)
                .limit(1)
            )

            the_most_populated_location_query = await session.execute(the_most_populated_location_query)
            the_less_populated_location_query = await session.execute(the_less_populated_location_query)

            the_most_populated_location = the_most_populated_location_query.scalars().first()
            the_less_populated_location = the_less_populated_location_query.scalars().first()

        if the_most_populated_location and the_less_populated_location:
            return the_most_populated_location.as_dict(), the_less_populated_location.as_dict()
        else:
            raise NotFoundException("No locations found.")

    async def get_unique_regions(self):
        async with self.__database_instance.session() as session:
            unique_regions_query = select(LocationsOrm.region).distinct()
            unique_regions = [region for region in (await session.execute(unique_regions_query)).scalars()]

        if unique_regions:
            return unique_regions
        else:
            raise NotFoundException("No regions found.")

    async def get_extreme_locations_for_all_regions(self) -> dict:
        unique_regions = await self.get_unique_regions()
        extreme_locations = {}

        for region_name in unique_regions:
            biggest_location, smallest_location = await self.get_extreme_locations(region_name)
            extreme_locations[region_name] = [biggest_location, smallest_location]

        return extreme_locations
