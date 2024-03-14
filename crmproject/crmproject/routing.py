from django.urls import path
from crmapp.consumers import ListingConsumer

websocket_urlpatterns = [
    path('myapp/', ListingConsumer.as_asgi())
] # тут наверное 'ws/crmapp', это путь оказывается ссылки, как views