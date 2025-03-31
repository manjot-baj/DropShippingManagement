import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
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
            return render(
                request, "vendor/products/product_list.html", {"products": products}
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching products."},
                status=500,
            )


# Create a new product with multiple image uploads
class ProductCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def validate_images(self, images):
        """Validate multiple image uploads."""
        allowed_extensions = (".jpg", ".jpeg", ".png")
        max_size = 5 * 1024 * 1024  # 5MB

        for image in images:
            if image.size > max_size:
                raise ValidationError("Each image must be less than 5MB.")
            if not image.name.lower().endswith(allowed_extensions):
                raise ValidationError("Only JPG and PNG images are allowed.")

    def get(self, request, *args, **kwargs):
        form = ProductForm(user=request.user)
        return render(request, "vendor/products/product_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = ProductForm(request.POST, request.FILES, user=request.user)
            images = request.FILES.getlist("images")

            # Validate images before saving
            try:
                self.validate_images(images)
            except ValidationError as e:
                messages.error(request, e.message)
                return render(
                    request, "vendor/products/product_form.html", {"form": form}
                )

            if form.is_valid():
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.vendor = get_object_or_404(
                        UserProfile, user=request.user, role="Vendor"
                    )
                    product.save()

                    for image in images:
                        ProductImage.objects.create(product=product, image=image)

                return redirect("product_list")
            return render(request, "vendor/products/product_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating product."},
                status=500,
            )


# Update an existing product
class ProductUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def validate_images(self, images):
        """Validate multiple image uploads."""
        allowed_extensions = (".jpg", ".jpeg", ".png")
        max_size = 5 * 1024 * 1024  # 5MB

        for image in images:
            if image.size > max_size:
                raise ValidationError("Each image must be less than 5MB.")
            if not image.name.lower().endswith(allowed_extensions):
                raise ValidationError("Only JPG and PNG images are allowed.")

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
        images = ProductImage.objects.filter(product=product)
        form = ProductForm(instance=product, user=request.user)
        return render(
            request,
            "vendor/products/product_form.html",
            {"form": form, "product": product, "images": images},
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
            form = ProductForm(
                request.POST, request.FILES, instance=product, user=request.user
            )
            images = request.FILES.getlist("images")

            # Validate images before saving
            try:
                self.validate_images(images)
            except ValidationError as e:
                messages.error(request, e.message)
                return render(
                    request,
                    "vendor/products/product_form.html",
                    {"form": form, "product": product},
                )

            if form.is_valid():
                with transaction.atomic():
                    product = form.save()
                    for image in images:
                        ProductImage.objects.create(product=product, image=image)

                return redirect("product_list")
            return render(
                request,
                "vendor/products/product_form.html",
                {"form": form, "product": product},
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating product."},
                status=500,
            )


# Delete a product (and related images)
class ProductDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=pk, vendor__user=request.user)
            product.delete()
            return JsonResponse(
                {"success": True, "message": "Product deleted successfully."}
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": "Error deleting product."}, status=500
            )


# Delete an image from a product
class ProductImageDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, image_id, *args, **kwargs):
        try:
            image = get_object_or_404(
                ProductImage, id=image_id, product__vendor__user=request.user
            )
            image.delete()
            return JsonResponse(
                {"success": True, "message": "Image deleted successfully."}
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": "Error deleting image."}, status=500
            )
