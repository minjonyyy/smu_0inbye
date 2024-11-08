import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs'].get('room_id')
        
        # room_id가 없는 경우에 대한 예외 처리
        if not self.room_id:
            await self.close()
            return
        
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender_email = text_data_json.get('sender_email')

        # room group에 메시지와 sender_email 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_email': sender_email
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        sender_email = event.get('sender_email') 

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_email': sender_email  
        }))
