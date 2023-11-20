from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Tournament
from channels.db import database_sync_to_async
from django.core.serializers import serialize
import json

# Сделайте функцию, которая сериализует ваши данные перед отправкой:
@database_sync_to_async
def serialize_tournaments():
    # serialize('json', ...) возвращает JSON-строку, представляющую QuerySet
    return serialize('json', Tournament.objects.all())

class TournamentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Присоединение к группе WebSocket
        await self.channel_layer.group_add(
            "tournament_updates",
            self.channel_name
        )
        # Принять WebSocket соединение
        await self.accept()
        # Получить и отправить текущие данные о турнирах клиенту
        serialized_tournaments = await serialize_tournaments()
        await self.send_json({
            "type": "initial_data",
            "message": serialized_tournaments
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "tournament_updates",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        serialized_tournaments = await serialize_tournaments()
        await self.send_json(serialized_tournaments)

    async def update_tournament(self, event):
        await self.send_json(event['message'])
