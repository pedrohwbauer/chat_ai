from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("chat_ai_app.chat.urls")),
    path('admin/', admin.site.urls),
]
