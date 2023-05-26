from django.db import models
from contracts.models import Contract
from status.models import Status
from users.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    contract = models.ForeignKey(
        Contract,
        limit_choices_to={"status": True},
        on_delete=models.CASCADE,
        related_name="event"
    )
    support_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "support"}
    )
    status = models.ForeignKey(
        Status,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events"   
    )
    attendees = models.PositiveIntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"Event #{self.id} : ({self.status})"