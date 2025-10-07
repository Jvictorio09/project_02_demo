from django.contrib import admin
from .models import Property, Lead


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "price_amount",
        "beds",
        "baths",
        "commissionable",
        "created_at",
    )
    search_fields = ("title", "city", "area", "badges", "affiliate_source")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "buy_or_rent",
        "budget_max",
        "beds",
        "utm_source",
        "created_at",
    )
    search_fields = ("name", "phone", "email", "areas", "interest_ids", "utm_source")


