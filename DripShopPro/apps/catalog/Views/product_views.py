import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Product, ProductImage
from catalog.Forms.product_forms import ProductForm
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")  # Centralized logger


# List all products (for vendor)
class ProductListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.select_related("vendor").filter(
                vendor__user=request.user
            )
            return render(request, "products/product_list.html", {"products": products})
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "error.html",
                {"message": "Error fetching products."},
                status=500,
            )


# Create a new product with multiple image uploads
class ProductCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        form = ProductForm(user=request.user)
        return render(request, "products/product_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = ProductForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.vendor = get_object_or_404(
                        UserProfile, user=request.user, role="Vendor"
                    )
                    product.save()

                    images = request.FILES.getlist("images")
                    for image in images:
                        ProductImage.objects.create(product=product, image=image)

                return redirect("product_list")
            return render(request, "products/product_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "error.html",
                {"message": "Error creating product."},
                status=500,
            )


# Update an existing product
class ProductUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
        form = ProductForm(instance=product, user=request.user)
        return render(
            request, "products/product_form.html", {"form": form, "product": product}
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
            form = ProductForm(
                request.POST, request.FILES, instance=product, user=request.user
            )
            if form.is_valid():
                with transaction.atomic():
                    product = form.save()
                    images = request.FILES.getlist("images")
                    for image in images:
                        ProductImage.objects.create(product=product, image=image)

                return redirect("product_list")
            return render(
                request,
                "products/product_form.html",
                {"form": form, "product": product},
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "error.html",
                {"message": "Error updating product."},
                status=500,
            )


# Delete a product (and related images)
class ProductDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
        return render(
            request, "products/product_confirm_delete.html", {"product": product}
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
            with transaction.atomic():
                product.delete()
            return redirect("product_list")
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "error.html",
                {"message": "Error deleting product."},
                status=500,
            )


# Delete an image from a product
class ProductImageDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, image_id, *args, **kwargs):
        image = get_object_or_404(
            ProductImage, id=image_id, product__vendor__user=request.user
        )
        return render(
            request, "products/product_image_confirm_delete.html", {"image": image}
        )

    def post(self, request, image_id, *args, **kwargs):
        try:
            image = get_object_or_404(
                ProductImage, id=image_id, product__vendor__user=request.user
            )
            product_id = image.product.id
            with transaction.atomic():
                image.delete()
            return redirect("product_update", pk=product_id)
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request, "error.html", {"message": "Error deleting image."}, status=500
            )
