import asyncio
import pandas as pd

from exceptions import NotFoundException
from orm import AsyncOrm


def convert_to_data_frame(data: list):
    df = pd.DataFrame(data)

    pd.set_option('display.max_columns', None)

    print(df)


async def main():
    try:
        all_locations = await AsyncOrm().select_all_locations()

        extreme_locations = await AsyncOrm().get_extreme_locations_for_all_regions()

        print('All the locations in short:')
        convert_to_data_frame(all_locations)

        for extreme_location in extreme_locations:
            print(f'\nThe most populated[0] and less populated[1] locations in {extreme_location} region:')
            convert_to_data_frame(extreme_locations[extreme_location])

    except NotFoundException as exception:
        print(exception)

if __name__ == "__main__":
    asyncio.run(main())
