from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email_id', 'role', 'mobile_no', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('username', 'email_id', 'mobile_no')
    ordering = ('username',)
    readonly_fields = ('user',)  # Ensures the linked User model cannot be edited

admin.site.register(UserProfile, UserProfileAdmin)
