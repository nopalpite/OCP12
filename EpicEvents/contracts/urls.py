from rest_framework_nested import routers
from .views import ContractViewSet

contracts = routers.DefaultRouter()
contracts.register(r'contracts', ContractViewSet, basename='contracts')

urlpatterns = contracts.urls
