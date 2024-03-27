import asyncio
import re


from DTOs import RegionDTO
from orm import AsyncOrm
from web_scrapper import Scrapper


class DataParser:
    async def __parse_data(self, bs4_instance) -> list[RegionDTO]:
        table = bs4_instance.find('table')
        table_rows = table.find_all('tr')
        list_of_regions = []

        for table_row in table_rows:
            table_datas = table_row.find_all('td')
            is_first_row = True
            region = []
            for table_data in table_datas:
                if is_first_row and len(table_datas) == 7:
                    is_first_row = False
                    continue

                cleaned_text = table_data.get_text(strip=True)

                if cleaned_text == '' or re.fullmatch(r'\[([a-zA-Z]+)\]', cleaned_text):
                    continue

                if re.fullmatch(r'\d{1,3}(,\d{3})*', cleaned_text):
                    cleaned_text = int(cleaned_text.replace(',', ''))
                elif cleaned_text == 'N/A':
                    cleaned_text = None

                region.append(cleaned_text)

            if len(region) == 6:
                regions = RegionDTO(*region)
                list_of_regions.append(regions)

        return list_of_regions

    async def fill_db(self):
        scrapper = Scrapper()
        bs4_instance = await scrapper.get_website_content(
            'https://en.wikipedia.org/w/'
            'index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959'
        )
        list_of_regions = await self.__parse_data(bs4_instance)

        async_orm_instance = AsyncOrm()

        await asyncio.gather(
            *[async_orm_instance.insert_location_data(region) for region in list_of_regions]
        )


async def main():
    await AsyncOrm().create_database()
    parser = DataParser()
    await parser.fill_db()


if __name__ == '__main__':
    asyncio.run(main())
