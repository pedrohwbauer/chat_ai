from channels.generic.websocket import AsyncWebsocketConsumer


class HTMLConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.group_name = f"turbo_stream.{group_name}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def html_message(self, event):
        """
        Send Turbo Stream html back to the client
        """
        html = event["html"]
        await self.send(text_data=html)