from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        *BaseUserAdmin.list_display,
        "user_type",
    )

    list_filter = (
        *BaseUserAdmin.list_filter,
        "user_type",
    )

    fieldsets = (*BaseUserAdmin.fieldsets, (None, {"fields": ("user_type",)}))


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "logo",
        "base_price",
        "min_price",
        "max_price",
        "percent_over_speeding",
        "min_speed_commit_rotate_head",
        "percent_head_rotate_for_hour",
        "max_speed_discount",
        "max_speed_penalty",
        "max_rotate_head_discount",
        "max_rotate_head_penalty",
    )

    fields = list_display
    readonly_fields = ("id",)
    list_filter = ("owner",)
    search_fields = ("id", "name", "logo", "base_price")
