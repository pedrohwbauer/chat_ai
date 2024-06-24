from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from .models import Chat, Message


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