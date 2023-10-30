import ast
import requests
url = "https://fs.nimbase.cc/v1/events/live-list"
headers = {
            'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
            'x-mashape-user': 'baggio093',
            'x-mashape-subscription': 'baggio093-Mega'
        }
params = {
            'timezone': '-4',
            'sport_id': '4',
            'locale': 'ru_RU'
        }
response = requests.get(url, headers=headers, params=params)
parsed_data = response.json()
print(parsed_data)