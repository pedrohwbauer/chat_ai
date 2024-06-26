from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect

from .models import Chat, Message
from .forms import MessageForm

from turbo_response import TurboStream, TurboStreamResponse

import openai
openai.api_key = '****************'


def get_ai_response(message_pk):
    chat_instance = Message.objects.get(pk=message_pk).chat
    message_instance = Message.objects.create(
        role=Message.ASSISTANT,
        content="",
        chat=chat_instance,
    )
    messages = Message.for_openai(chat_instance.messages.all())

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        message_instance.content = response['choices'][0]['message']['content']
        message_instance.save(update_fields=["content"])
    except Exception as e:
        message_instance.content = str(e)
        message_instance.save(update_fields=["content"])

    # return AI message
    return message_instance


class IndexView(View):

    def get(self, request):
        # If no chat exists, create a new chat and redirect to the message list page.
        chat = Chat.objects.first()
        if not chat:
            chat = Chat.objects.create()
        return HttpResponseRedirect(reverse("chat:message-list", args=[chat.pk]))

    def post(self, request, *args, **kwargs):
        # create new chat object and redirect to message list view
        instance = Chat.objects.create()
        return HttpResponseRedirect(reverse("chat:message-list", args=[instance.pk]))


index_view = IndexView.as_view()


class MessageListView(ListView):
    model = Message
    template_name = "message_list_page.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(chat_id=self.kwargs["chat_pk"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chats"] = Chat.objects.all()
        return context


message_list_view = MessageListView.as_view()


class MessageCreateView(CreateView):
    model = Message
    template_name = "message_create.html"
    form_class = MessageForm

    def get_success_url(self):
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["chat_pk"] = self.kwargs.get("chat_pk")
        kwargs["role"] = Message.USER
        return kwargs

    def get_empty_form(self):
        """
        Return empty form so we can reset the form
        """
        form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs.pop("data")
        kwargs.pop("files")
        kwargs.pop("instance")
        return form_class(**kwargs)

    def form_valid(self, form):
        super().form_valid(form)
        request = self.request

        ai_message = get_ai_response(self.object.pk)

        # return Turbo Stream to do partial updates on the page
        return TurboStreamResponse(
            [
                TurboStream("message-create-frame")
                    .replace.template(
                    self.template_name,
                    {
                        "form": self.get_empty_form(),
                        "request": request,
                        "view": self,
                    },
                ).response(request).rendered_content,
                # user message
                TurboStream(f"chat-{self.kwargs['chat_pk']}-message-list")
                    .append.template(
                    "message_item.html",
                    {
                        "instance": self.object,
                    },
                ).response(request).rendered_content,
                # AI message
                TurboStream(f"chat-{self.kwargs['chat_pk']}-message-list")
                    .append.template(
                    "message_item.html",
                    {
                        "instance": ai_message,
                    },
                ).response(request).rendered_content,
            ]
        )



message_create_view = MessageCreateView.as_view()