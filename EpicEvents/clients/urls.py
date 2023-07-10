from django.urls import path, include
from rest_framework_nested import routers
from .views import ClientViewSet
import pprint
clients = routers.DefaultRouter()
clients.register(r'clients', ClientViewSet, basename='clients')

urlpatterns = clients.urls

pprint.pprint(clients.get_urls())