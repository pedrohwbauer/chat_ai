from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.db.transaction import on_commit
from django.dispatch import receiver
from turbo_response import TurboStream

from chat_ai_app.chat.tasks import task_chat_gpt, task_chat_llm

from .models import Message


@receiver(post_save, sender=Message)
def handle_user_message(sender, instance, created, **kwargs):
    html = (
        TurboStream(f"chat-{instance.chat.pk}-message-list")
            .append.template(
            "message_item.html",
            {
                "instance": instance,
                "turbo_stream": True,
            },
        ).render()
    )
    channel_layer = get_channel_layer()
    group_name = f"turbo_stream.chat_{instance.chat.pk}"
    async_to_sync(channel_layer.group_send)(
        group_name, {"type": "html_message", "html": html}
    )

    if created and instance.role == Message.USER:
        message_instance = Message.objects.create(
            role=Message.ASSISTANT,
            content="Thinking...",
            chat=instance.chat,
        )

        # call openai chat task in Celery worker
        # on_commit(lambda: task_chat_gpt.delay(message_instance.pk))
        
        on_commit(lambda: task_chat_llm.delay(message_instance.pk))
        