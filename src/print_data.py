import asyncio
import pandas as pd

from exceptions import NotFoundException
from orm import AsyncOrm


def convert_to_data_frame(data: list):
    df = pd.DataFrame(data)

    pd.set_option('display.max_columns', None)

    less_columned_df = df.iloc[:, 1:3]

    print(less_columned_df)


async def main():
    try:
        the_most_populated_location = await AsyncOrm().select_the_most_populated_location()
        the_less_populated_location = await AsyncOrm().select_the_less_populated_location()
        all_locations = await AsyncOrm().select_all_locations()

        print('All the locations in short:')
        convert_to_data_frame(all_locations)

        print('\nThe most populated location:')
        convert_to_data_frame(the_most_populated_location)

        print('\nThe less populated location:')
        convert_to_data_frame(the_less_populated_location)

    except NotFoundException as exception:
        print(exception)

if __name__ == "__main__":
    asyncio.run(main())
