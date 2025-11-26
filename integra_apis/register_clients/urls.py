from django.urls import path
from .views import ClienteList, ClienteDetail, ChatList, UserList, UserDetail

urlpatterns = [
    path("clientes/", ClienteList.as_view(), name="client_list"),
    path("clientes/<str:pk>/", ClienteDetail.as_view(), name="client_detail"),
    path("users/", UserList.as_view(), name="user_list"),
    path("users/<str:pk>/", UserDetail.as_view(), name="user_detail"),
    path("chats/", ChatList.as_view(), name="chat_list"),
]
