from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from user_profile.middlewares import role_required
from catalog.models import Product, ProductImage
from catalog.Forms.product_forms import ProductForm
from user_profile.models import UserProfile


# List all products (for vendor)
@role_required("Vendor")
def product_list(request):
    products = Product.objects.select_related("vendor").filter(
        vendor__user=request.user
    )  # Filter by vendor
    return render(request, "products/product_list.html", {"products": products})


# Create a new product with multiple image uploads
@role_required("Vendor")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                product = form.save(commit=False)
                product.vendor = get_object_or_404(
                    UserProfile, user=request.user, role="Vendor"
                )  # Set vendor
                product.save()  # Ensure product is saved before adding images

                # Save multiple images
                images = request.FILES.getlist("images")
                for image in images:
                    ProductImage.objects.create(product=product, image=image)

            return redirect("product_list")
    else:
        form = ProductForm(user=request.user)

    return render(request, "products/product_form.html", {"form": form})


# Update an existing product (also update images if provided)
@role_required("Vendor")
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor__user=request.user)

    if request.method == "POST":
        form = ProductForm(
            request.POST, request.FILES, instance=product, user=request.user
        )
        if form.is_valid():
            with transaction.atomic():
                product = form.save()

                # If new images are provided, save them
                images = request.FILES.getlist("images")
                for image in images:
                    ProductImage.objects.create(product=product, image=image)

            return redirect("product_list")
    else:
        form = ProductForm(instance=product, user=request.user)

    return render(
        request, "products/product_form.html", {"form": form, "product": product}
    )


# Delete a product (also delete related images)
@role_required("Vendor")
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor__user=request.user)

    if request.method == "POST":
        with transaction.atomic():
            product.delete()  # Automatically deletes related images due to cascade
            return redirect("product_list")

    return render(
        request, "products/product_confirm_delete.html", {"product": product}
    )  # Show confirmation page


# Delete an image from a product
@role_required("Vendor")
def product_image_delete(request, image_id):
    image = get_object_or_404(
        ProductImage, id=image_id, product__vendor__user=request.user
    )
    product_id = image.product.id

    if request.method == "POST":
        with transaction.atomic():
            image.delete()
            return redirect("product_update", product_id)

    return render(
        request, "products/product_image_confirm_delete.html", {"image": image}
    )  # Show confirmation page
