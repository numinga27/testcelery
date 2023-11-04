from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .task import send_request

class TournamentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        # Запускаем задачу обновления данных в фоновом режиме
        send_request.delay()

    async def update_tournament(self, event):
        # Отправляем обновленные данные клиенту
        await self.send_json(event["text"])
