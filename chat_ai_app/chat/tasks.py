from django.conf import settings

from openai import OpenAI
client = OpenAI(
  api_key=settings.OPENAI_KEY,
)

from celery import shared_task

from .models import Message


@shared_task(name="task_ai_chat")
def task_ai_chat(message_pk):
    message_instance = Message.objects.get(pk=message_pk)
    chat_instance = message_instance.chat

    messages = Message.for_openai(chat_instance.messages.all())

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            stream=True,
        )

        # iterate through the stream of events
        for index, chunk in enumerate(response):
            if index == 0:
                # clear content and ready to display response from OpenAI
                message_instance.content = ""

            content = getattr(chunk.choices[0].delta, "content", None)
            if content is not None:
                message_instance.content += content
                message_instance.save(update_fields=["content"])

    except Exception as e:
        message_instance.content += str(e)
        message_instance.save(update_fields=["content"])
