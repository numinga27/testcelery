import requests
import ast
import http
import json
import logging
import datetime
from datetime import timedelta


from .models import (Events, Tournament, HockeyLiveEvents,
                     TournamentHockey, EndedMatch, Scheduled, All, AllHockey,
                     ScheduledHockey, EndedHockey, EventId)
from .serialiazers import EventsSerializer, HockeyLiveEventsSerializer
from django.db import transaction
from requests.exceptions import RequestException
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def upload_image(s):
    url = 'https://static.stat.bet/api/upload'
    data = {
        'api_key': 'f99454e5d9c51487bb4e051e9ed5875b545df1dd90d859820b4387a4666fda8b',
        'photo_url': s
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        data = response.json()
        uploaded_url = data['path']
        return uploaded_url
    else:
        print(f"Ошибка {response.status_code}: {response.text}")


@shared_task
def delete():
    Tournament.objects.all().delete()
    Events.objects.all().delete()
    TournamentHockey.objects.all().delete()
    HockeyLiveEvents.objects.all().delete()


@shared_task
def send_request(bind=True, autoretry_for=(RequestException,), retry_backoff=True):
    logging.basicConfig(filename="app.log", filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    result = []
    # delete()
    try:

        Tournament.objects.all().select_for_update().delete()
        Events.objects.all().select_for_update().delete()
        url = "https://fs.nimbase.cc/v1/events/live-list"
        headers = {
            'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
            'x-mashape-user': 'baggio093',
            'x-mashape-subscription': 'baggio093-Mega'
        }
        params = {
            'timezone': '-4',
            'sport_id': '1',
            'locale': 'ru_RU'
        }
        response = requests.get(url, headers=headers, params=params)
        parsed_data = response.json()
        # print(parsed_data)
        try:
            for item in parsed_data['DATA']:
                # tournaments = Tournament.objects.filter(name=item['NAME'])
                # # if tournaments.exists():
                # #     tournament = tournaments.first()
                # # else:
                tournament_imng = upload_image(
                    item['TOURNAMENT_IMAGE'])
                # print(tournament_imng)
                tournament_data = {
                    'name': item['NAME'],
                    'tournament_stage_type': item['TOURNAMENT_STAGE_TYPE'],
                    'tournament_imng': str(tournament_imng),
                    'TOURNAMENT_TEMPLATE_ID': item['TOURNAMENT_TEMPLATE_ID']
                }
                tournament, created = Tournament.objects.update_or_create(
                    TOURNAMENT_TEMPLATE_ID=item['TOURNAMENT_TEMPLATE_ID'],
                    defaults=tournament_data
                )
                for event in item['EVENTS']:
                    home_img = [upload_image(
                        event.get('HOME_IMAGES'))]
                    away_img = [upload_image(event.get('AWAY_IMAGES'))]
                    # print(home_img, away_img)
                    stage_start_time = datetime.datetime.fromtimestamp(
                        event['STAGE_START_TIME'])
                    current_time = datetime.datetime.now() - stage_start_time
                    data = {
                        'event_id': event['EVENT_ID'],
                        'start_time': event['START_TIME'],
                        'start_utime': event['START_UTIME'],
                        'game_time': event['GAME_TIME'],
                        'short_name_away': event['SHORTNAME_AWAY'],
                        'away_name': event['AWAY_NAME'],
                        'away_score_current': event['AWAY_SCORE_CURRENT'],
                        'away_score_part_1': event['AWAY_SCORE_PART_1'],
                        'away_score_part_2': event.get('AWAY_SCORE_PART_2', ''),
                        'short_name_home': event['SHORTNAME_HOME'],
                        'home_name': event['HOME_NAME'],
                        'home_score_current': event['HOME_SCORE_CURRENT'],
                        'home_score_part_1': event['HOME_SCORE_PART_1'],
                        'home_score_part_2': event.get('HOME_SCORE_PART_2', ''),
                        'home_images': event.get('HOME_IMAGES'),
                        'away_images': event.get('AWAY_IMAGES'),
                        'stge_type': event['STAGE_TYPE'],
                        'merge_stage_tupe': event['MERGE_STAGE_TYPE'],
                        'stage': event['STAGE'],
                        'sort': event['SORT'],
                        'live_mark': event['LIVE_MARK'],
                        'red_cards_home': event.get('HOME_RED_CARDS', 0),
                        'red_cards_away': event.get('AWAY_RED_CARDS', 0),
                        'stage_start_time': event['STAGE_START_TIME'],
                        'current_time': str(current_time)
                    }
                    if event['STAGE'] == "SECOND_HALF":
                        current_time += timedelta(minutes=45)
                        data['current_time'] = str(current_time)
                    data['away_images'] = away_img
                    data['home_images'] = home_img
                    serializer = EventsSerializer(data=data)
                    if serializer.is_valid():
                        event_object, created = Events.objects.update_or_create(
                            event_id=event['EVENT_ID'], defaults=serializer.validated_data)
                        tournament.events.add(event_object)
                    else:
                        print(serializer.errors)
        except KeyError:
            pass
        # event_ids = Events.objects.values_list('event_id', flat=True)
        # for event_idss in event_ids:
        #     EventId.objects.update_or_create(live_event_id=event_idss)
        # conn = http.client.HTTPSConnection(
        #     "fs.nimbase.cc")

        # headers = {
        #     'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
        #     'x-mashape-user': 'baggio093',
        #     'x-mashape-subscription': 'baggio093-Mega'
        # }

        # for event_idss in event_ids:
        #     try:
        #         conn.request(
        #             "GET", f"/v1/events/statistics?event_id={event_idss}&locale=ru_RU", headers=headers)
        #         res = conn.getresponse()
        #         data = res.read()
        #         json_data = json.loads(data)
        #         for item in json_data['DATA'][0]['GROUPS'][0]['ITEMS']:
        #             if item["INCIDENT_NAME"] == "Yellow Cards":
        #                 yellow_cards_home = item['VALUE_HOME']
        #                 yellow_cards_away = item['VALUE_AWAY']
        #                 break
        #         event = Events.objects.get(event_id=event_idss)
        #         event.yellow_cards_home = yellow_cards_home
        #         event.yellow_cards_away = yellow_cards_away
        #         event.save()
        #     except Exception:
        #         pass
    except Exception as e:
        # Если возникла ошибка, записываем ее в лог
        logger.error("Произошла ошибка при получении матчей: %s", e)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "live_updates",  # это имя группы, которое вы использовали в consumer'е
        {
            "type": "update_tournament",  # это имя метода в вашем consumer'е
            "message": Tournament.objects.all()
        }
    )
    # return Tournament.objects.all()


@shared_task
def send_request_hockey(bind=True, autoretry_for=(RequestException,), retry_backoff=True):
    # # try:
    # with transaction.atomic():
    TournamentHockey.objects.all().select_for_update().delete()
    HockeyLiveEvents.objects.all().select_for_update().delete()
    

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
    try:
        for item in parsed_data['DATA']:

            # tournament = TournamentHockey.objects.filter(
            #     name=item['NAME'])
            # if tournament.exists():
            #     tournament = tournament.first()
            # else:
            tournament_img = upload_image(
                item['TOURNAMENT_IMAGE'])
            tournament_data = {
                'name': item['NAME'],
                'tournament_stage_type': item['TOURNAMENT_STAGE_TYPE'],
                'tournament_imng': str(tournament_img),
                'TOURNAMENT_TEMPLATE_ID': item['TOURNAMENT_TEMPLATE_ID']
            }
            tournament, created = TournamentHockey.objects.update_or_create(
                TOURNAMENT_TEMPLATE_ID=item['TOURNAMENT_TEMPLATE_ID'],
                defaults=tournament_data
            )
            for event in item['EVENTS']:
                home_img = [upload_image(
                    event.get('HOME_IMAGES'))]
                away_img = [upload_image(event.get('AWAY_IMAGES'))]
                data = {
                    'events_id': event['EVENT_ID'],
                    'start_time': event['START_TIME'],
                    'start_utime': event['START_UTIME'],
                    'game_time': event['GAME_TIME'],
                    'shortname_away': event['SHORTNAME_AWAY'],
                    'away_name': event['AWAY_NAME'],
                    'away_current_score': event['AWAY_SCORE_CURRENT'],
                    'away_score_part_1': event['AWAY_SCORE_PART_1'],
                    'away_score_part_2': event.get('AWAY_SCORE_PART_2', ''),
                    'away_images': event.get('AWAY_IMAGES', ''),
                    'shortname_home': event['SHORTNAME_HOME'],
                    'home_name': event['HOME_NAME'],
                    'home_current_score': event['HOME_SCORE_CURRENT'],
                    'home_score_part_1': event['HOME_SCORE_PART_1'],
                    'home_score_part_2': event.get('HOME_SCORE_PART_2', ''),
                    'home_images': event.get('HOME_IMAGES', ''),
                    'stge_type': event['STAGE_TYPE'],
                    'merge_stage_tupe': event['MERGE_STAGE_TYPE'],
                    'stage': event['STAGE'],
                    'sort': event['SORT'],
                    'live_mark': event['LIVE_MARK'],
                    'has_lineps': event['HAS_LINEPS'],
                    'stage_start_time': event['STAGE_START_TIME'],
                    'playing_in_sets': event['PLAYING_ON_SETS'],
                    'recent_overs': event['RECENT_OVERS'],
                    'home_participant_name_one': event['HOME_PARTICIPANT_NAME_ONE'],
                    'home_event_participant_id': event['HOME_EVENT_PARTICIPANT_ID'],
                    'home_goal_var': event['HOME_GOAL_VAR'],
                    'home_score_part_3': event.get('HOME_SCORE_PART_3', ''),
                    'away_participant_name_one': event['AWAY_PARTICIPANT_NAME_ONE'],
                    'away_event_participant_id': event['AWAY_EVENT_PARTICIPANT_ID'],
                    'away_goal_var': event['AWAY_GOAL_VAR'],
                    'away_score_fullL': event['AWAY_SCORE_FULL'],
                    'away_score_part_3': event.get('AWAY_SCORE_PART_3', '')
                }
                data['away_images'] = away_img
                data['home_images'] = home_img
                serializer = HockeyLiveEventsSerializer(data=data)
                if serializer.is_valid():
                    event_object, created = HockeyLiveEvents.objects.update_or_create(
                        events_id=event['EVENT_ID'], defaults=serializer.validated_data)
                    tournament.events.add(event_object)
                    # event_objects = HockeyLiveEvents.objects.filter(
                    #     events_id=event['EVENT_ID'])
                    # if event_objects.exists():
                    #     event_object = event_objects.first()
                    #     serializer.update(
                    #         event_object, serializer.validated_data)
                    # else:
                    #     event_object = HockeyLiveEvents.objects.create(
                    #         **serializer.validated_data)
                    # tournament.events.add(event_object)
                else:
                    print(serializer.errors)
    except KeyError:
        pass
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)('tournament', {'type': 'update_tournament', 'text': "updated_data"})
    return TournamentHockey.objects.all()


@shared_task
def send_request_endedmatch():
    try:
        with transaction.atomic():
            EndedMatch.objects.all().select_for_update().delete()
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
            try:
                for item in parsed_data['DATA']:
                    ended_match = EndedMatch.objects.filter(
                        tournamet_name=item['NAME'])
                    if ended_match.exists():
                        ended_match = ended_match.first()
                    else:
                        ended_match = EndedMatch.objects.create(
                            tournamet_name=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE'],
                            stage_type=item['TOURNAMENT_STAGE_TYPE']
                        )
                    for event in item['EVENTS']:
                        if event.get("STAGE_TYPE") == "FINISHED" or event.get("STAGE_TYPE") == "3":
                            ended_match.event_id = event.get("EVENT_ID")
                            ended_match.round = event.get("ROUND")
                            ended_match.shortname_home = event.get(
                                "SHORTNAME_HOME")
                            ended_match.home_name = event.get("HOME_NAME")
                            ended_match.home_score_current = event.get(
                                "HOME_SCORE_CURRENT")
                            ended_match.home_score_part_1 = event.get(
                                "HOME_SCORE_PART_1")
                            ended_match.home_score_part_2 = event.get(
                                "HOME_SCORE_PART_2", '')
                            ended_match.home_images = event.get("HOME_IMAGES")
                            ended_match.shortname_away = event.get(
                                "SHORTNAME_AWAY")
                            ended_match.name_away = event.get("AWAY_NAME")
                            ended_match.away_score_current = event.get(
                                "AWAY_SCORE_CURRENT")
                            ended_match.away_score_full = event.get(
                                "AWAY_SCORE_FULL")
                            ended_match.away_score_part_1 = event.get(
                                "AWAY_SCORE_PART_1")
                            ended_match.away_score_part_2 = event.get(
                                "AWAY_SCORE_PART_2", '')
                            ended_match.away_images = event.get("AWAY_IMAGES")

                            ended_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass


@shared_task
def send_request_scheluded():
    try:
        with transaction.atomic():
            Scheduled.objects.all().select_for_update().delete()
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
            try:
                for item in parsed_data['DATA']:
                    scheduled_match = Scheduled.objects.filter(
                        tournament=item['NAME'])
                    if scheduled_match.exists():
                        scheduled_match = scheduled_match.first()
                    else:
                        scheduled_match = Scheduled.objects.create(
                            tournament=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE']
                        )
                    for event in item['EVENTS']:
                        if event.get("STAGE_TYPE") == "SCHEDULED" or event.get("STAGE_TYPE") == "1":
                            scheduled_match.event_id = event.get('EVENT_ID')
                            scheduled_match.start_time = event.get(
                                'START_TIME')
                            scheduled_match.start_utime = event.get(
                                'START_UTIME')
                            scheduled_match.shortname_home = event.get(
                                'SHORTNAME_HOME')
                            scheduled_match.home_name = event.get('HOME_NAME')
                            scheduled_match.home_images = event.get(
                                'HOME_IMAGES', '')
                            scheduled_match.shortname_away = event.get(
                                'SHORTNAME_AWAY')
                            scheduled_match.name_away = event.get('AWAY_NAME')
                            scheduled_match.away_images = event.get(
                                'AWAY_IMAGES', '')

                            scheduled_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass


@shared_task
def request_all():
    try:
        with transaction.atomic():
            All.objects.all().select_for_update().delete()
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
            try:
                for item in parsed_data['DATA']:
                    ended_match = All.objects.filter(
                        tournamet_name=item['NAME'])
                    if ended_match.exists():
                        ended_match = ended_match.first()
                    else:
                        ended_match = All.objects.create(
                            tournamet_name=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE'],
                            stage_type=item['TOURNAMENT_STAGE_TYPE']
                        )
                    for event in item['EVENTS']:
                        ended_match.event_id = event.get("EVENT_ID")
                        ended_match.round = event.get("ROUND")
                        ended_match.shortname_home = event.get(
                            "SHORTNAME_HOME")
                        ended_match.home_name = event.get("HOME_NAME")
                        ended_match.home_score_current = event.get(
                            "HOME_SCORE_CURRENT")
                        ended_match.home_score_part_1 = event.get(
                            "HOME_SCORE_PART_1")
                        ended_match.home_score_part_2 = event.get(
                            "HOME_SCORE_PART_2", '')
                        ended_match.home_images = event.get("HOME_IMAGES")
                        ended_match.shortname_away = event.get(
                            "SHORTNAME_AWAY")
                        ended_match.name_away = event.get("AWAY_NAME")
                        ended_match.away_score_current = event.get(
                            "AWAY_SCORE_CURRENT")
                        ended_match.away_score_full = event.get(
                            "AWAY_SCORE_FULL")
                        ended_match.away_score_part_1 = event.get(
                            "AWAY_SCORE_PART_1")
                        ended_match.away_score_part_2 = event.get(
                            "AWAY_SCORE_PART_2", '')
                        ended_match.away_images = event.get("AWAY_IMAGES")

                        ended_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass


@shared_task
def request_all_hockey():
    try:
        with transaction.atomic():
            AllHockey.objects.all().select_for_update().delete()
            url = "https://fs.nimbase.cc/v1/events/list"
            querystring = {"timezone": "-4", "indent_days": "-1",
                           "locale": "ru_RU", "sport_id": "4"}
            headers = {
                'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
                'x-mashape-user': 'baggio093',
                'x-mashape-subscription': 'baggio093-Mega'
            }
            response = requests.get(url, headers=headers, params=querystring)
            parsed_data = response.json()
            try:
                for item in parsed_data['DATA']:
                    ended_match = AllHockey.objects.filter(
                        tournamet_name=item['NAME'])
                    if ended_match.exists():
                        ended_match = ended_match.first()
                    else:
                        ended_match = AllHockey.objects.create(
                            tournamet_name=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE'],
                            stage_type=item['TOURNAMENT_STAGE_TYPE']
                        )
                    for event in item['EVENTS']:
                        ended_match.event_id = event.get("EVENT_ID")
                        ended_match.round = event.get("ROUND")
                        ended_match.shortname_home = event.get(
                            "SHORTNAME_HOME")
                        ended_match.home_name = event.get("HOME_NAME")
                        ended_match.home_score_current = event.get(
                            "HOME_SCORE_CURRENT")
                        ended_match.home_score_part_1 = event.get(
                            "HOME_SCORE_PART_1")
                        ended_match.home_score_part_2 = event.get(
                            "HOME_SCORE_PART_2", '')
                        ended_match.home_images = event.get("HOME_IMAGES")
                        ended_match.shortname_away = event.get(
                            "SHORTNAME_AWAY")
                        ended_match.name_away = event.get("AWAY_NAME")
                        ended_match.away_score_current = event.get(
                            "AWAY_SCORE_CURRENT")
                        ended_match.away_score_full = event.get(
                            "AWAY_SCORE_FULL")
                        ended_match.away_score_part_1 = event.get(
                            "AWAY_SCORE_PART_1")
                        ended_match.away_score_part_2 = event.get(
                            "AWAY_SCORE_PART_2", '')
                        ended_match.away_score_part_3 = event.get(
                            "AWAY_SCORE_PART_3", '')
                        ended_match.away_images = event.get("AWAY_IMAGES")
                        ended_match.home_score_part_3 = event.get(
                            "HOME_SCORE_PART_3", '')

                        ended_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass


@shared_task
def request_scheduled_hockey():
    try:
        with transaction.atomic():
            ScheduledHockey.objects.all().select_for_update().delete()
            url = "https://fs.nimbase.cc/v1/events/list"
            querystring = {"timezone": "-4", "indent_days": "-1",
                           "locale": "ru_RU", "sport_id": "4"}
            headers = {
                'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
                'x-mashape-user': 'baggio093',
                'x-mashape-subscription': 'baggio093-Mega'
            }
            response = requests.get(url, headers=headers, params=querystring)
            parsed_data = response.json()
            try:
                for item in parsed_data['DATA']:
                    scheduled_match = ScheduledHockey.objects.filter(
                        tournament=item['NAME'])
                    if scheduled_match.exists():
                        scheduled_match = scheduled_match.first()
                    else:
                        scheduled_match = ScheduledHockey.objects.create(
                            tournament=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE']
                        )
                    for event in item['EVENTS']:
                        if event.get("STAGE_TYPE") == "SCHEDULED" or event.get("STAGE_TYPE") == "1":
                            scheduled_match.event_id = event.get('EVENT_ID')
                            scheduled_match.start_time = event.get(
                                'START_TIME')
                            scheduled_match.start_utime = event.get(
                                'START_UTIME')
                            scheduled_match.shortname_home = event.get(
                                'SHORTNAME_HOME')
                            scheduled_match.home_name = event.get('HOME_NAME')
                            scheduled_match.home_images = event.get(
                                'HOME_IMAGES', '')
                            scheduled_match.shortname_away = event.get(
                                'SHORTNAME_AWAY')
                            scheduled_match.name_away = event.get('AWAY_NAME')
                            scheduled_match.away_images = event.get(
                                'AWAY_IMAGES', '')

                            scheduled_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass


@shared_task
def request_ended_hockey():
    try:
        with transaction.atomic():
            EndedHockey.objects.all().select_for_update().delete()
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
            try:
                for item in parsed_data['DATA']:
                    ended_match = EndedHockey.objects.filter(
                        tournamet_name=item['NAME'])
                    if ended_match.exists():
                        ended_match = ended_match.first()
                    else:
                        ended_match = EndedHockey.objects.create(
                            tournamet_name=item['NAME'],
                            tournament_imng=item['TOURNAMENT_IMAGE'],
                            stage_type=item['TOURNAMENT_STAGE_TYPE']
                        )
                    for event in item['EVENTS']:
                        if event.get("STAGE_TYPE") == "FINISHED" or event.get("STAGE_TYPE") == "3":
                            ended_match.event_id = event.get("EVENT_ID")
                            ended_match.round = event.get("ROUND")
                            ended_match.shortname_home = event.get(
                                "SHORTNAME_HOME")
                            ended_match.home_name = event.get("HOME_NAME")
                            ended_match.home_score_current = event.get(
                                "HOME_SCORE_CURRENT")
                            ended_match.home_score_part_1 = event.get(
                                "HOME_SCORE_PART_1")
                            ended_match.home_score_part_2 = event.get(
                                "HOME_SCORE_PART_2", '')
                            ended_match.home_score_part_3 = event.get(
                                "HOME_SCORE_PART_3", '')
                            ended_match.home_images = event.get("HOME_IMAGES")
                            ended_match.shortname_away = event.get(
                                "SHORTNAME_AWAY")
                            ended_match.name_away = event.get("AWAY_NAME")
                            ended_match.away_score_current = event.get(
                                "AWAY_SCORE_CURRENT")
                            ended_match.away_score_full = event.get(
                                "AWAY_SCORE_FULL")
                            ended_match.away_score_part_1 = event.get(
                                "AWAY_SCORE_PART_1")
                            ended_match.away_score_part_2 = event.get(
                                "AWAY_SCORE_PART_2", '')
                            ended_match.away_score_part_3 = event.get(
                                "AWAY_SCORE_PART_3", '')
                            ended_match.away_images = event.get("AWAY_IMAGES")

                            ended_match.save()
            except KeyError:
                # Обработка ошибки KeyError
                pass
    except Exception:
        pass
