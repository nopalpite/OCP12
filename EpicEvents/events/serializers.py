from rest_framework.serializers import ModelSerializer
from .models import Event

class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "name",
            "location",
            "contract",
            "status",
            "attendees",
            "event_date",
            "notes"
        ]
        read_only_fields = ["date_created", "date_updated", "support_contact"]
