from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_ai_app.chat'

    def ready(self):
        from chat_ai_app.chat import receivers