from rest_framework_nested import routers
from .views import EventViewSet

events = routers.DefaultRouter()
events.register(r'events', EventViewSet, basename='events')

urlpatterns = events.urls
