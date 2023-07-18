from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contract


class ContractPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "support":
            return request.method in SAFE_METHODS
        return request.user.role == "sales"

    def has_object_permission(self, request, view, obj):
        if request.user.role == "support" and request.method in SAFE_METHODS:
            contracts = Contract.objects.filter(
                event__support_contact=request.user
            )
            return obj in contracts
        return obj.sales_contact == request.user
