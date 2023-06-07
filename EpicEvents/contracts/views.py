from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import ContractSerializer
from .models import Contract
from .permissions import ContractPermission

class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]

    def get_queryset(self):
        if self.request.user.role == "support":
            contracts = Contract.objects.filter(
                event__support_contact=self.request.user
            )
            return contracts
        elif self.request.user.role == "sales":
            contracts = Contract.objects.filter(sales_contact=self.request.user)
            return contracts