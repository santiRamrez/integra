from django.urls import path
from .views import ClienteAPIView

urlpatterns = [
    path("", ClienteAPIView.as_view(), name="client_list"),
]
