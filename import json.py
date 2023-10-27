import ast
import requests
def upload_image(s):
    url = 'https://static.stat.bet/api/upload'
    data = {
    'api_key':'f99454e5d9c51487bb4e051e9ed5875b545df1dd90d859820b4387a4666fda8b',
    'photo_url':ast.literal_eval(s)
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        data = response.json()
        uploaded_url = data['path']
        return uploaded_url
    else:
        print(f"Ошибка {response.status_code}: {response.text}")

print(upload_image('["https://www.flashscore.com/res/image/data/pKDeVgld-SKnSoRTH.png"]'))