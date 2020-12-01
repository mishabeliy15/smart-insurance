from contracts.models import Contract, Offer
from django.contrib import admin


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "customer",
        "end_date",
        "personal_coefficient",
    )

    fields = list_display
    list_filter = (
        "company",
        "customer",
        "end_date",
    )
    search_fields = list_filter


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "company",
        "customer",
        "months",
        "personal_coefficient",
    )

    fields = list_display
    list_filter = (
        "company",
        "customer",
        "months",
    )
    search_fields = list_filter
