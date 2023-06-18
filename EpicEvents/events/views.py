from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer
from .models import Event
from .permissions import EventPermission

class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermission]
    filterset_fields = [
        'contract__client__last_name',
        'contract__client__email',
        'event_date'
    ]

    def get_queryset(self):
        if self.request.user.role == "support":
            events = Event.objects.filter(
                support_contact=self.request.user
            )
            return events
        elif self.request.user.role == "sales":
            events = Event.objects.filter(contract__sales_contact=self.request.user)
            return events