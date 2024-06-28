import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat_ai_app.chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_ai_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(
        routing.urlpatterns
    )
})