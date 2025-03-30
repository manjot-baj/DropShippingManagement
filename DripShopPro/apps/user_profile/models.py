from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("Merchant", "Merchant"),
        ("Vendor", "Vendor"),
        ("Customer", "Customer"),
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    otp = models.CharField(max_length=10, blank=True, null=True)
    email_id = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=12, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # vendor merchant oriented fields
    is_approved = models.BooleanField(default=False)
    is_plan_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    plan_start_date = models.DateField(null=True, blank=True)
    plan_expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
