from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email_id",
        "role",
        "mobile_no",
        "is_approved",
        "is_plan_active",
        "created_at",
        "plan_start_date",
        "plan_expiry_date",
    )

    list_filter = (
        "role",
        "is_approved",
        "is_plan_active",
    )
    search_fields = ("username", "email_id", "mobile_no")
    ordering = ("created_at",)
    readonly_fields = ("user",)  # Ensures the linked User model cannot be edited


admin.site.register(UserProfile, UserProfileAdmin)
