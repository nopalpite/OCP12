from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Client


class ClientPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "support":
            return request.method in SAFE_METHODS
        return request.user.role == "sales"

    def has_object_permission(self, request, view, obj):
        if request.user.role == "support" and request.method in SAFE_METHODS:
            clients = Client.objects.filter(
                contract__event__support_contact=request.user
            )
            return obj in clients
        return obj.sales_contact == request.user
