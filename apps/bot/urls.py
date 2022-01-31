from django.urls import path
from django.conf import settings

from apps.bot.views import handle

urlpatterns = [
    path(f'{settings.BOT_TOKEN}/', handle)
]