from django.urls import path

from chat_ai_app.chat import consumers


urlpatterns = [
    path("ws/turbo_stream/<group_name>/", consumers.HTMLConsumer.as_asgi()),
]