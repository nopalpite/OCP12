from rest_framework.serializers import ModelSerializer
from .models import Contract

class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = [
            "client",
            "status",
            "amount",
            "payment_due"
        ]
        read_only_fields = ["sales_contact", "date_created", "date_updated"]