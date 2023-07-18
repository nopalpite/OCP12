from django.contrib import admin
from .models import Status


@admin.register(Status)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Status",
            {
                "fields": (
                    "name",
                )
            },
        ),
    )
    list_display = (
        "name",
    )
    list_filter = ("name",)
    search_fields = ("name",)
