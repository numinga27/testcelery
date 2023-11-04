import ast
import requests
url = "https://fs.nimbase.cc/v1/events/list"
querystring = {"timezone": "-4", "indent_days": "-1",
                           "locale": "ru_RU", "sport_id": "1"}
headers = {
                'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
                'x-mashape-user': 'baggio093',
                'x-mashape-subscription': 'baggio093-Mega'
            }
response = requests.get(url, headers=headers, params=querystring)
parsed_data = response.json()
print(parsed_data)