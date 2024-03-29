from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Event Info",
            {
                "fields": (
                    "name",
                    "location",
                    "contract",
                    "attendees",
                    "event_date",
                    "status",
                )
            },
        ),
        ("Support", {"fields": ("support_contact", "notes")}),
        ("Info", {"fields": ("date_created", "date_updated")}),
    )
    readonly_fields = ("date_created", "date_updated")
    list_display = (
        "id",
        "name",
        "location",
        "contract",
        "support_contact",
        "attendees",
        "event_date",
        "status",
    )
    list_filter = ("status", "support_contact")
    search_fields = ("name", "location", "client__last_name")
