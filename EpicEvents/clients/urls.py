from django.urls import path, include
from rest_framework_nested import routers
from .views import ClientViewSet
clients = routers.DefaultRouter()
clients.register(r'clients', ClientViewSet, basename='clients')

urlpatterns = clients.urls
