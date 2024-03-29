import json
import urllib.request as r
from urllib.error import HTTPError


def get_data(city):
    try:
        data = r.urlopen('https://restcountries.eu/rest/v2/capital/' + city).read()
        print_data(json.loads(data)[0], city)
    except HTTPError:
        pass


def print_data(json_data, city):
    print('\n------------------------------')
    print('Here is the information about ' + city + ':')
    print('Country:', json_data['name'])
    print('Borders:', json_data['borders'])
    print('Population:', json_data['population'])
    print('------------------------------')


if __name__ == '__main__':
    arr = [
        'bratislava', 'prague', 'stockholm', 'tokyo', 'budapest', 'berlin',
        'vienna', 'canberra', 'moscow', 'minsk', 'ottawa', 'dublin'
    ]

    import time
    start = time.time()
    for city_input in arr:
        get_data(city_input)
    end = time.time()
    print('Time elapsed:', end - start)
