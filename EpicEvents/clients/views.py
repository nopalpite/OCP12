from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import ClientSerializer
from .models import Client
from .permissions import ClientPermission


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        if self.request.user.role == "support":
            clients = Client.objects.filter(
                contract__event__support_contact=self.request.user
            )
            return clients
        elif self.request.user.role == "sales":
            clients = Client.objects.filter(sales_contact=self.request.user)
            return clients
