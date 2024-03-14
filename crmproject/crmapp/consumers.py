from channels.generic.websocket import AsyncWebsocketConsumer
import json

# передача данных нового объявления
class ListingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Подключение")
        await self.channel_layer.group_add("listings", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("listings", self.channel_name)

    async def receive(self, text_data):
        # Вы можете получать данные здесь, если будете использовать двунаправленный WebSocket
        pass

    async def listing_message(self, event):
        print(f"Отправка данных: {event['listing']}")
        # Отправка данных объявления клиенту через WebSocket
        await self.send(text_data=json.dumps({
            'type': 'listing_message',
            'listing': event['listing']
        }))

    # из PhoneConsumer взял, ранее функция sync_status была там
    async def sync_status(self, event):
        # Обработка сообщения о статусе синхронизации
        print('SYNC_STATUS')
        status_message = event['message']
        await self.send(text_data=json.dumps({'type': 'sync_status', 'message': status_message}))