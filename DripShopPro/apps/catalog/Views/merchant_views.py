import logging
import traceback
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from store.models import Store, StoreProduct
from catalog.models import Company

logger = logging.getLogger("error_log")


class MerchantListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            company_pk_list = Company.objects.filter(
                owner__user=request.user
            ).values_list("pk", flat=True)

            products = StoreProduct.objects.filter(
                inventory__company__pk__in=company_pk_list
            )
            store_pk_list = products.values_list("store__pk", flat=True)

            merchants = Store.objects.filter(pk__in=store_pk_list)

            merchant_list = [
                {
                    "name": f"{merchant.owner.first_name} {merchant.owner.last_name }",
                    "store": merchant.name,
                    "email": merchant.email,
                    "phone": merchant.phone,
                    "state": merchant.state,
                    "products_in_store": StoreProduct.objects.filter(
                        inventory__company__pk__in=company_pk_list, store=merchant
                    ).count(),
                }
                for merchant in merchants
            ]

            return render(
                request,
                "vendor/products/merchant_list.html",
                {"merchants": merchant_list},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching store.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching store."},
                status=500,
            )
