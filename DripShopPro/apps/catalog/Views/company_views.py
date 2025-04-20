import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from catalog.Utils.middlewares import CompanyRequiredMixin
from catalog.models import Company
from catalog.Forms.company_forms import CompanyForm
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")


class CompanyListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            company = Company.objects.select_related("owner").filter(
                owner__user=request.user,
                is_deleted=False,
            )
            return render(
                request, "vendor/company/company_list.html", {"companys": company}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


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

                messages.success(request, "Company created successfully.")
                return redirect("company_list")

            messages.error(request, "Invalid form submission.")
            return render(request, "vendor/company/company_form.html", {"form": form})

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating company.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating company."},
                status=500,
            )


class CompanyUpdateView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        try:
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
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching company.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching company."},
                status=500,
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
                    form.save()

                messages.success(request, "Company updated successfully.")
                return redirect("company_list")

            messages.error(request, "Invalid form submission.")
            return render(
                request,
                "vendor/company/company_form.html",
                {"form": form, "company": company},
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating company.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating company."},
                status=500,
            )


class CompanyDeleteView(RoleRequiredMixin, CompanyRequiredMixin, View):
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
            messages.success(request, "Company deleted successfully.")
            return JsonResponse(
                {"success": True, "message": "Company deleted successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error deleting company.")
            return JsonResponse(
                {"success": False, "message": "Error deleting company."}, status=500
            )
