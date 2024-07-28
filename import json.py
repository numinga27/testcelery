import json
import requests

url = "https://fs.nimbase.cc/v1/events/live-list"
headers = {
    'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
    'x-mashape-user': 'baggio093',
    'x-mashape-subscription': 'baggio093-Mega'
}
params = {
    'timezone': '-4',
    'sport_id': '1',
    'locale': 'en_INT'
}
response = requests.get(url, headers = headers, params = params)
parsed_data = response.json()
print(parsed_data)
#': 1, 'STAGE_START_TIME': 1698091542, 'GAME_TIME': None, 'PLAYING_ON_SETS': None, 'RECENT_OVERS': None, 'SHORTNAME_AWAY': 'CAD', 'AWAY_PARTICIPANT_IDS': ['hdWjLJUJ'], 'AWAY_PARTICIPANT_TYPES': [1], 'AWAY_NAME': 'Cadiz CF', 'AWAY_PARTICIPANT_NAME_ONE': 'Cadiz CF', 'AWAY_EVENT_PARTICIPANT_ID': 'K6gFgE9f', 'AWAY_RED_CARDS': 1, 'AWAY_GOAL_VAR': 0, 'AWAY_SCORE_CURRENT': '0', 'AWAY_SCORE_FULL': 0, 'AWAY_SCORE_PART_1': '0', 'AWAY_SCORE_PART_2': '0', 'AWAY_IMAGES': ['https://www.flashscore.com/res/image/data/0Q4qMJeM-EPWyZtpb.png'], 'IMM': 'CQeaytrD', 'IMW': '100', 'IMP': 'Ioshoye5-MHrRLNUo.png', 'IME': '', 'SHORTNAME_HOME': 'VAL', 'HOME_PARTICIPANT_IDS': ['CQeaytrD'], 'HOME_PARTICIPANT_TYPES': [1], 'HOME_NAME': 'Valencia', 'HOME_PARTICIPANT_NAME_ONE': 'Valencia', 'HOME_EVENT_PARTICIPANT_ID': 'QqfBfffl', 'HOME_GOAL_VAR': 0, 'HOME_SCORE_CURRENT': '2', 'HOME_SCORE_PART_1': '2', 'HOME_SCORE_PART_2': '0', 'HOME_IMAGES': ['https://www.flashscore.com/res/image/data/Ioshoye5-MHrRLNUo.png'], 'TV_LIVE_STREAMING': {'1': [{'TVI': 1025, 'BU': 'https://viaplay.com/gb-en/sport', 'BN': 'Viaplay (UK)'}], '2': [{'BU': '/bookmaker/417/?from=live-streaming&sport=1', 'IU': '/res/image/data/bookmakers/17-417.png', 'BN': '1xBet', 'BI': 417}, {'BU': '/bookmaker/16/?from=live-streaming&sport=1',