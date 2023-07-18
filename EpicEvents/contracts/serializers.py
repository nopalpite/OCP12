from rest_framework.serializers import ModelSerializer
from .models import Contract


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["id", "sales_contact",
                            "date_created", "date_updated"]
