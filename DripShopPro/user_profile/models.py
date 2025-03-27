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
    is_approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "Customer":
            self.is_approved = True
        self.user.is_active = self.is_approved
        self.user.save()
        super().save(*args, **kwargs)
