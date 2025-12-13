import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ehealth.models import Consultation, ChatMessage, NewUser
from channels.db import database_sync_to_async

# -------------------------
# CHAT CONSUMER
# -------------------------

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.consultation_id = self.scope["url_route"]["kwargs"]["consultation_id"]
        self.room_group = f"chat_{self.consultation_id}"

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_email = data["sender"]

        await self.save_message(sender_email, message)

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_email,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_email, message):
        sender = NewUser.objects.get(email=sender_email)
        consultation = Consultation.objects.get(id=self.consultation_id)
        ChatMessage.objects.create(
            consultation=consultation,
            sender=sender,
            message=message
        )


# -------------------------
# NOTIFICATION CONSUMER
# -------------------------

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.room_group = f"notify_{self.user.id}"

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))
