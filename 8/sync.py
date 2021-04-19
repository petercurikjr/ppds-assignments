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
    print('------------------------------')


if __name__ == '__main__':
    import time

    inp = '_'
    arr = []
    while inp != '':
        inp = input('Enter a list of capital city names of your choice: ')
        arr.append(inp)

    start = time.time()
    for city_input in arr:
        get_data(city_input)
    end = time.time()
    print('Time elapsed:', end - start)
