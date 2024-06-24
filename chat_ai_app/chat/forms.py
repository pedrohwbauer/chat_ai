from django import forms

from .models import Chat, Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop("role")
        self.chat_pk = kwargs.pop("chat_pk")

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.chat_id = self.chat_pk
        instance.role = self.role
        if commit:
            instance.save()
        return instance