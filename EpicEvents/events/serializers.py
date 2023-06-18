from rest_framework.serializers import ModelSerializer
from .models import Event

class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id", "date_created", "date_updated", "support_contact"]
