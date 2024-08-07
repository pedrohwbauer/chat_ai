from django.conf import settings

from django.db.models import Subquery, OuterRef

from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat, Message
from .forms import MessageForm

from turbo_response import TurboStream, TurboStreamResponse

class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        # If no chat exists, create a new chat and redirect to the message list page.
        chat = Chat.objects.filter(user=request.user).first()
        if not chat:
            chat = Chat.objects.create(user=request.user)
        return HttpResponseRedirect(reverse("chat:message-list", args=[chat.pk]))

    def post(self, request, *args, **kwargs):
        # create new chat object and redirect to message list view
        instance = Chat.objects.create(user=request.user)
        return HttpResponseRedirect(reverse("chat:message-list", args=[instance.pk]))


index_view = IndexView.as_view()


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list_page.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(chat_id=self.kwargs["chat_pk"], chat__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Define the subquery
        last_messages = Message.objects.filter(chat=OuterRef('pk')).order_by('-created_at')

        # Annotate the chats with the last message content
        chats = Chat.objects.filter(user=self.request.user).annotate(
            last_message_content=Subquery(last_messages.values('content')[:1])
        )
        
        context['chats'] = chats

        return context


message_list_view = MessageListView.as_view()


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "message_create.html"
    form_class = MessageForm

    def get_success_url(self):
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["chat_pk"] = self.kwargs.get("chat_pk")
        kwargs["role"] = Message.USER
        kwargs["user"] = self.request.user
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
            ]
        )


message_create_view = MessageCreateView.as_view()