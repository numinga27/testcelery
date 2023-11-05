from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .task import send_request
from asgiref.sync import async_to_sync
import json

class TournamentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Вызов функции обновления
        async_to_sync(send_request)()

    async def update_tournament(self, event):
        # Отправляем обновленные данные клиенту
        await self.send_json(event["text"])
