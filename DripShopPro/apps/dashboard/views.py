import logging
import traceback
from django.shortcuts import render
from user_profile.models import UserProfile
from catalog.models import Category
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages

logger = logging.getLogger("error_log")


class VendorDashboardView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            return render(request, f"vendor/dashboard.html", {"user": user})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class MerchantDashboardView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            return render(request, f"merchant/dashboard.html", {"user": user})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class CustomerDashboardView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            categorys = Category.objects.all()
            return render(
                request,
                f"customer/dashboard.html",
                {"user": user, "categorys": categorys},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )
