import http.client
import asyncio
import requests
import time
import schedule
import threading
import json

from django.db import transaction
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import (Events, EventId, Tournament, TournamentHockey, EndedMatch,
                     Scheduled, All, AllHockey, ScheduledHockey, EndedHockey)
from .serialiazers import (EventsSerializer, EventLiveIdSerializer,
                           TournamentSerializer, TournamentHockeySerializer, EndedMatchSerializer,
                           ScheduledSerializer, AllSerializer, AllHockeySerializer,
                           ScheduledHockeySerializer, EndedHockeySerializer)
from .task import (send_request, send_request_hockey,
                   send_request_endedmatch, send_request_scheluded, request_all,
                   request_all_hockey, request_scheduled_hockey)

import http.client


class EventIdViewSet(viewsets.ModelViewSet):
    queryset = EventId.objects.all()
    serializer_class = EventLiveIdSerializer

    # def list_ev(self, request):
    #     # Удаление данных из таблицы
    #     EventId.objects.all().delete()
    #     event_ids = Events.objects.values_list('event_id', flat=True)
    #     for event_id in event_ids:
    #         live_event = EventId(live_event_id=event_id)
    #         live_event.save()

    # async def send_request(self):
    #     self.list(None)

    # async def schedule_request(self):
    #     while True:
    #         await self.send_request()  # Выполняем запрос
    #         await asyncio.sleep(0.33)  # Подождать 0.33 секунды

    # def start_scheduling(self):
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(self.schedule_request())
    #     loop.run_forever()


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


def h2h(live_event_id):
    conn = http.client.HTTPSConnection("fs.nimbase.cc")
    headers = {
        'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
        'x-mashape-user': 'baggio093',
        'x-mashape-subscription': 'baggio093-Mega'
    }
    url = f"/v1/events/h2h?locale=en_INT&event_id={live_event_id}"
    url = url.replace(" ", "")
    print(url)
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def events_statistic(live_event_id):
    conn = http.client.HTTPSConnection("fs.nimbase.cc")

    headers = {
        'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
        'x-mashape-user': 'baggio093',
        'x-mashape-subscription': 'baggio093-Mega'
    }
    # encoded_event_id = quote(event_id.encode('utf-8'), safe='')
    url = f"/v1/events/statistics?event_id={live_event_id}&locale=en_INT"
    url = url.replace(" ", "")
    conn.request(
        "GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def events_start_lineps(live_event_id):

    conn = http.client.HTTPSConnection("fs.nimbase.cc")

    headers = {
        'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
        'x-mashape-user': 'baggio093',
        'x-mashape-subscription': 'baggio093-Mega'
    }
    url = f"/v1/events/lineups?event_id={live_event_id}&locale=en_INT"
    url = url.replace(" ", "")
    conn.request(
        "GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def odds(live_event_id):
    conn = http.client.HTTPSConnection("fs.nimbase.cc")

    headers = {
        'api-key-bravo': 'Nc4znHJeSs06G99YMVVBovHF',
        'x-mashape-user': 'baggio093',
        'x-mashape-subscription': 'baggio093-Mega'
    }

    url = f"/v1/events/odds?event_id={live_event_id}&locale=en_INT"
    url = url.replace(" ", "")
    conn.request(
        "GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


class EventDetails(APIView):
    '''Вью для деталей матча '''
    # permission_classes = AllowAny

    def get(self, request, live_event_id):
        event = get_object_or_404(EventId, live_event_id=live_event_id)
        h2h_data = h2h(event.live_event_id)
        statistics_data = events_statistic(event.live_event_id)
        lineups = events_start_lineps(event.live_event_id)
        odd = odds(event.live_event_id)

        serialized_data = json.dumps(
            {'statistics_data': statistics_data}, {'h2h': h2h_data}, {'lineups': lineups}, {'odd': odd})

        return Response(serialized_data)


class TournamentViewSet(viewsets.ModelViewSet):
    ''' Основаной вью для лайва'''
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    # def start_scheduling(self):
    #     # Запускаем функцию send_request каждые 5 секунд
    #     schedule.every(2).seconds.do(send_request)
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(0.05)

    # def list(self, request):
    #     # Запускаем поток для выполнения start_scheduling
    #     thread = threading.Thread(target=self.start_scheduling)
    #     thread.start()
    #     tournaments = Tournament.objects.all()
    #     serializer = self.serializer_class(tournaments, many=True)
    #     # event_viewset = EventIdViewSet()
    #     # event_viewset.list_ev(request)
    #     return Response(serializer.data)
    def list(self, request):
        task = send_request()  # Add parentheses to call the function
        serializer = self.serializer_class(task, many=True)
        return Response(serializer.data)

        


class HockeyView(viewsets.ModelViewSet):
    '''Основной вью для хоккея'''
    queryset = TournamentHockey.objects.all()
    serializer_class = TournamentHockeySerializer

    # def start_scheduling(self):
    #     # Запускаем функцию send_request каждые 5 секунд
    #     schedule.every(5).seconds.do(send_request_hockey)
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)

    # def list(self, request):
    #     # Запускаем поток для выполнения start_scheduling
    #     thread = threading.Thread(target=self.start_scheduling)
    #     thread.start()
    #     tournaments_hockey = TournamentHockey.objects.all()
    #     serializer = self.serializer_class(tournaments_hockey, many=True)
    #     # event_viewset = EventIdViewSet()
    #     # event_viewset.list_ev(request)
    #     return Response(serializer.data)
    def list(self, request):
        task = send_request_hockey()  # Add parentheses to call the function
        serializer = self.serializer_class(task, many=True)
        return Response(serializer.data)


class EndedMatchView(viewsets.ModelViewSet):
    queryset = EndedMatch.objects.all()
    serializer_class = EndedMatchSerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(send_request_endedmatch)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = EndedMatch.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)


class ScheduledView(viewsets.ModelViewSet):
    queryset = Scheduled.objects.all()
    serializer_class = ScheduledSerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(send_request_scheluded)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = Scheduled.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)


class AllView(viewsets.ModelViewSet):
    queryset = All.objects.all()
    serializer_class = AllSerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(request_all)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = All.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)


class AllHockeyView(viewsets.ModelViewSet):
    queryset = AllHockey.objects.all()
    serializer_class = AllHockeySerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(request_all_hockey)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = AllHockey.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)


class ScheduledHockeyView(viewsets.ModelViewSet):
    queryset = ScheduledHockey.objects.all()
    serializer_class = ScheduledHockeySerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(request_scheduled_hockey)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = ScheduledHockey.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)


class EndedHockeyView(viewsets.ModelViewSet):
    queryset = EndedHockey.objects.all()
    serializer_class = EndedHockeySerializer

    def start_scheduling(self):
        # Запускаем функцию send_request каждые 5 секунд
        schedule.every(50).seconds.do(request_scheduled_hockey)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list(self, request):
        # Запускаем поток для выполнения start_scheduling
        thread = threading.Thread(target=self.start_scheduling)
        thread.start()
        tournaments = EndedHockey.objects.all()
        serializer = self.serializer_class(tournaments, many=True)

        return Response(serializer.data)
