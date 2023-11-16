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
    groups = ["tournament_updates"]

    # ... Ваш код connect и disconnect ...

    # В методе receive не вызывайте send_request напрямую, т.к это синхронный метод.
    async def receive(self, text_data):
        # Получите уже сериализованные данные для отправки
        serialized_tournaments = await serialize_tournaments()

        # Send message to room group
        await self.channel_layer.group_send(
            "tournament_updates",
            {
                'type': 'update_tournament',
                'message': serialized_tournaments,
            }
        )

async def update_tournament(self, event):
    # Get the message from the event and send it out to the WebSocket
    message = event['message']
