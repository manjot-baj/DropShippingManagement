import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Product, ProductImage, Category
from catalog.Forms.product_forms import ProductForm, CategoryForm
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")


class CategoryListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            categorys = Category.objects.select_related("vendor").filter(
                vendor__user=request.user, is_deleted=False
            )
            return render(
                request, "vendor/products/category_list.html", {"categorys": categorys}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching categories.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching categories."},
                status=500,
            )


class CategoryCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            form = CategoryForm(user=request.user)
            return render(request, "vendor/products/category_form.html", {"form": form})
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching category form.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching category form."},
                status=500,
            )

    def post(self, request, *args, **kwargs):
        try:
            form = CategoryForm(request.POST, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    category = form.save(commit=False)
                    category.vendor = get_object_or_404(
                        UserProfile, user=request.user, role="Vendor"
                    )
                    category.save()
                messages.success(request, "Category created successfully.")
                return redirect("category_list")

            messages.error(request, "Invalid form submission.")
            return render(request, "vendor/products/category_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating category.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating category."},
                status=500,
            )


class CategoryUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        try:
            category = get_object_or_404(
                Category, pk=pk, vendor__user=request.user, is_deleted=False
            )
            form = CategoryForm(instance=category, user=request.user)
            return render(
                request,
                "vendor/products/category_form.html",
                {"form": form, "category": category},
            )
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching category.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching category."},
                status=500,
            )

    def post(self, request, pk, *args, **kwargs):
        try:
            category = get_object_or_404(
                Category, pk=pk, vendor__user=request.user, is_deleted=False
            )
            form = CategoryForm(request.POST, instance=category, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    category = form.save()
                messages.success(request, "Category updated successfully.")
                return redirect("category_list")

            messages.error(request, "Invalid form submission.")
            return render(
                request,
                "vendor/products/category_form.html",
                {"form": form, "category": category},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating category.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating category."},
                status=500,
            )


class CategoryDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, pk, *args, **kwargs):
        try:
            category = get_object_or_404(
                Category, pk=pk, vendor__user=request.user, is_deleted=False
            )
            category.is_deleted = True
            category.save()
            messages.success(request, "Category deleted successfully.")
            return JsonResponse(
                {"success": True, "message": "Category deleted successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error deleting category.")
            return JsonResponse(
                {"success": False, "message": "Error deleting category."}, status=500
            )


class ProductListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.select_related("vendor").filter(
                vendor__user=request.user, is_deleted=False
            )
            return render(
                request, "vendor/products/product_list.html", {"products": products}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching products.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching products."},
                status=500,
            )


class ProductCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def validate_images(self, images):
        allowed_extensions = (".jpg", ".jpeg", ".png")
        max_size = 5 * 1024 * 1024

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

                messages.success(request, "Product created successfully.")
                return redirect("product_list")

            messages.error(request, "Invalid product form.")
            return render(request, "vendor/products/product_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating product.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating product."},
                status=500,
            )


class ProductUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def validate_images(self, images):
        allowed_extensions = (".jpg", ".jpeg", ".png")
        max_size = 5 * 1024 * 1024

        for image in images:
            if image.size > max_size:
                raise ValidationError("Each image must be less than 5MB.")
            if not image.name.lower().endswith(allowed_extensions):
                raise ValidationError("Only JPG and PNG images are allowed.")

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(
            Product, pk=pk, vendor__user=request.user, is_deleted=False
        )
        images = ProductImage.objects.filter(product=product, is_deleted=False)
        form = ProductForm(instance=product, user=request.user)
        return render(
            request,
            "vendor/products/product_form.html",
            {"form": form, "product": product, "images": images},
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(
                Product, pk=pk, vendor__user=request.user, is_deleted=False
            )
            form = ProductForm(
                request.POST, request.FILES, instance=product, user=request.user
            )
            existing_images = ProductImage.objects.filter(
                product=product, is_deleted=False
            )
            images = request.FILES.getlist("images")

            try:
                self.validate_images(images)
            except ValidationError as e:
                messages.error(request, e.message)
                return render(
                    request,
                    "vendor/products/product_form.html",
                    {"form": form, "product": product, "images": existing_images},
                )

            if form.is_valid():
                with transaction.atomic():
                    product = form.save()
                    for image in images:
                        ProductImage.objects.create(product=product, image=image)

                messages.success(request, "Product updated successfully.")
                return redirect("product_list")

            messages.error(request, "Invalid product form.")
            return render(
                request,
                "vendor/products/product_form.html",
                {"form": form, "product": product, "images": existing_images},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating product.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating product."},
                status=500,
            )


class ProductDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(
                Product, pk=pk, vendor__user=request.user, is_deleted=False
            )
            product.is_deleted = True
            product.save()
            messages.success(request, "Product deleted successfully.")
            return JsonResponse(
                {"success": True, "message": "Product deleted successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error deleting product.")
            return JsonResponse(
                {"success": False, "message": "Error deleting product."}, status=500
            )


class ProductImageDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, image_id, *args, **kwargs):
        try:
            image = get_object_or_404(
                ProductImage,
                id=image_id,
                product__vendor__user=request.user,
                is_deleted=False,
            )
            image.is_deleted = True
            image.save()
            messages.success(request, "Image deleted successfully.")
            return JsonResponse(
                {"success": True, "message": "Image deleted successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error deleting image.")
            return JsonResponse(
                {"success": False, "message": "Error deleting image."}, status=500
            )
