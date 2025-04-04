import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Company
from catalog.Forms.company_forms import CompanyForm
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")  # Centralized logger


# List all company (for vendor)
class CompanyListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            company = Company.objects.select_related("owner").filter(
                owner__user=request.user,
                is_deleted=False,
            )
            return render(
                request, "vendor/company/company_list.html", {"company": company}
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching company."},
                status=500,
            )


# Create a new company
class CompanyCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        form = CompanyForm(user=request.user)
        return render(request, "vendor/company/company_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = CompanyForm(request.POST, request.FILES, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    company = form.save(commit=False)
                    company.owner = get_object_or_404(
                        UserProfile,
                        user=request.user,
                        role="Vendor",
                    )
                    company.save()

                return redirect("company_list")
            return render(request, "vendor/company/company_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating company."},
                status=500,
            )


# Update an existing company
class CompanyUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        company = get_object_or_404(
            Company,
            pk=pk,
            owner__user=request.user,
            is_deleted=False,
        )
        form = CompanyForm(instance=company, user=request.user)
        return render(
            request,
            "vendor/company/company_form.html",
            {"form": form, "company": company},
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            company = get_object_or_404(
                Company,
                pk=pk,
                owner__user=request.user,
                is_deleted=False,
            )
            form = CompanyForm(
                request.POST, request.FILES, instance=company, user=request.user
            )

            if form.is_valid():
                with transaction.atomic():
                    company = form.save()

                return redirect("company_list")
            return render(
                request,
                "vendor/company/company_form.html",
                {"form": form, "company": company},
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating company."},
                status=500,
            )


# Delete a company (and related images)
class CompanyDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, pk, *args, **kwargs):
        try:
            company = get_object_or_404(
                Company,
                pk=pk,
                owner__user=request.user,
                is_deleted=False,
            )
            company.is_deleted = True
            company.save()
            return JsonResponse(
                {"success": True, "message": "Company deleted successfully."}
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": "Error deleting company."}, status=500
            )
