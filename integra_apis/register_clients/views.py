from rest_framework import generics
from .models import Cliente, Chat
from .serializers import ClienteSerializer, ChatSerializer


class ClienteAPIView(generics.ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
