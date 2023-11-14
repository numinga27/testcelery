from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .task import send_request
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json

class TournamentConsumer(AsyncJsonWebsocketConsumer):
    groups = ["tournament_updates"]
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("tournament_updates", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("tournament_updates", self.channel_name)

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        message = send_request()

        # Send message to room group
        await self.channel_layer.group_send(
            "tournament_updates",
            {
                'type': 'update_tournament',
                'message': message,
            }
        )

    # Receive message from room group
    # async def update_tournament(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #     }))
    # @database_sync_to_async
    # def get_last_message(self)
    #     return Tournament.objects.all()