import json
import asyncio
import urllib.request as r
from urllib.error import HTTPError


async def get_data(city):
    try:
        data = r.urlopen('https://restcountries.eu/rest/v2/capital/' + city).read()
        print_data(json.loads(data)[0], city)
    except HTTPError:
        pass


def print_data(json_data, city):
    print('\n------------------------------')
    print('Here is the information about ' + city + ':')
    print('Country:', json_data['name'])
    print('------------------------------')


async def main():
    import time

    # arr = []
    arr = [
        'bratislava', 'prague', 'stockholm', 'tokyo', 'budapest', 'berlin',
        'vienna', 'canberra', 'moscow', 'minsk', 'ottawa', 'dublin'
    ]

    inp = '_'
    while inp != '' and len(arr) == 0:
        inp = input('Enter a list of capital city names of your choice: ')
        arr.append(inp)

    start = time.time()
    await asyncio.gather(*(get_data(city_input) for city_input in arr))
    end = time.time()
    print('Time elapsed:', end - start)


if __name__ == '__main__':
    asyncio.run(main())

