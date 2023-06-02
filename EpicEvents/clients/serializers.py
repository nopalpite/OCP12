from rest_framework.serializers import ModelSerializer
from .models import Client

class ClientSerializer(ModelSerializer):
    
    class Meta:
        model = Client
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "is_active"
        ]
        read_only_fields = ["sales_contact", "date_created", "date_updated"] 
