from rest_framework import generics
from django.contrib.auth.models import User
from .models import Cliente, Chat
from .serializers import ClienteSerializer, ChatSerializer, UserSerializer
from .permissions import IsUserOrReadOnly


class ClienteList(generics.ListCreateAPIView):
    permission_classes = (IsUserOrReadOnly,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsUserOrReadOnly,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializer
