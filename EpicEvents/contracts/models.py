from django.db import models
from users.models import User
from clients.models import Client
from status.models import Status

# Create your models here.
class Contract(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True},
        related_name="contracts"
    )
    sales_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "sales"},
        related_name="contracts"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        if self.status:
            stat = self.status
        else:
            stat = ""
        return f"Contract #{self.id} : ({stat})"