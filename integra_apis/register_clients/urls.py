from django.urls import path
from .views import ClienteAPIView, ChatList

urlpatterns = [
    path("clientes/", ClienteAPIView.as_view(), name="client_list"),
    path("chats/", ChatList.as_view(), name="chat_list"),
]
