from django.urls import path
from .views import ChatAPIView

urlpatterns = [
    path('conversa/', ChatAPIView.as_view(), name='chat-api'),
]