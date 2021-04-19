import json
import urllib.request as r


def get_data(city):
    data = r.urlopen('https://restcountries.eu/rest/v2/capital/' + city).read()
    print_data(json.loads(data)[0], city)


def print_data(json_data, city):
    print('\n------------------------------')
    print('Here is the information about ' + city + ':')
    print('Country:', json_data['name'])
    print('------------------------------\n')


if __name__ == '__main__':
    while True:
        inp = input('Enter a name of a capital city of your choice: ')
        get_data(inp)
