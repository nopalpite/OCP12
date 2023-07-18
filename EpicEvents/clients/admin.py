from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Client",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "company_name",
                    "email",
                    "phone",
                    "mobile",
                )
            },
        ),
        ("Sales", {"fields": ("is_active", "sales_contact")}),
        ("Info", {"fields": ("date_created", "date_updated")}),
    )
    readonly_fields = ("id", "date_created", "date_updated")
    list_display = (
        "id",
        "first_name",
        "last_name",
        "company_name",
        "email",
        "phone",
        "mobile",
        "is_active",
        "sales_contact",
    )
    list_filter = ("is_active", "sales_contact")
    search_fields = ("first_name", "last_name", "email",
                     "company_name", "sales_contact")
