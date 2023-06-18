from rest_framework.serializers import ModelSerializer
from .models import Client

class ClientSerializer(ModelSerializer):
    
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["id", "sales_contact", "date_created", "date_updated"] 
