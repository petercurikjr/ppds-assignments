import asyncio
from aiohttp import ClientSession


async def get_data(city):
    async with ClientSession() as s:
        async with s.get('https://restcountries.eu/rest/v2/capital/' + city) as r:
            print_data(await r.json(), city)


def print_data(data, city):
    data = data[0]
    print('\n------------------------------')
    print('Here is the information about ' + city + ':')
    print('Country:', data['name'])
    print('Borders:', data['borders'])
    print('Population:', data['population'])
    print('------------------------------')


async def main():
    arr = [
        'bratislava', 'prague', 'stockholm', 'tokyo', 'budapest', 'berlin',
        'vienna', 'canberra', 'moscow', 'minsk', 'ottawa', 'dublin'
    ]

    import time
    start = time.time()
    await asyncio.gather(*(get_data(city_input) for city_input in arr))
    end = time.time()
    print('Time elapsed:', end - start)


if __name__ == '__main__':
    asyncio.run(main())

