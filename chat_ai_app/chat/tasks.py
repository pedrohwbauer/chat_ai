from django.conf import settings

from openai import OpenAI
client = OpenAI(
  api_key=settings.OPENAI_KEY,
)

from celery import shared_task

from .models import Message


@shared_task(name="task_chat_gpt")
def task_chat_gpt(message_pk):
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
        
        
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM


# Load the Hugging Face model and tokenizer
model_name = "distilbert/distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
chat_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

@shared_task(name="task_chat_llm")
def task_chat_llm(message_pk):
    message_instance = Message.objects.get(pk=message_pk)
    chat_instance = message_instance.chat

    messages = Message.for_openai(chat_instance.messages.all())
    messages_text = "\n".join([msg['content'] for msg in messages])
    print(messages_text)
    try:
        # Generate response using the Hugging Face model
        response = chat_pipeline(messages_text, max_length=1000, num_return_sequences=1, truncate=True)

        # Process the response
        generated_text = response[0]['generated_text']

        # Save the generated text
        message_instance.content = generated_text
        message_instance.save(update_fields=["content"])

    except Exception as e:
        message_instance.content += str(e)
        message_instance.save(update_fields=["content"])