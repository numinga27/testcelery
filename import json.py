import ast
import requests
url = "https://flashlive-sports-api.hgapi.top/v1/events/live-list?locale=en_INT&sport_id=1&timezone=-4"
headers = {
  'accept': 'application/json' ,
  'x-portal-apikey': 'CJZtUTmTlzmYL2LOAXfMEdwpTTyskrM5hQhT4lT1DJqUz'
}

response = requests.get(url, headers=headers)
parsed_data = response.json() 
print(parsed_data)