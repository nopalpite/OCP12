from rest_framework.permissions import BasePermission, SAFE_METHODS

class EventPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "support":
            return request.method in ["GET", "PUT"]
        return request.user.role == "sales"
    
    def has_object_permission(self, request, view, obj):
        if  request.method in SAFE_METHODS:
            event = obj.contract.sales_contact or obj.support_contact
            return event
        else:
            if request.user.role == "support":
                return request.user == obj.support_contact
            return request.user == obj.contract.sales_contact
