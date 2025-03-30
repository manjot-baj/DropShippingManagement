from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Catalog
from catalog.Forms.catalog_forms import CatalogForm
from user_profile.middlewares import role_required


@role_required("Vendor")
def catalog_detail(request):
    catalog = Catalog.objects.filter(vendor=request.user.userprofile).first()
    return render(request, "catalog/catalog_detail.html", {"catalog": catalog})


@role_required("Vendor")
def catalog_create(request):
    vendor = request.user.userprofile
    if Catalog.objects.filter(vendor=vendor).exists():
        return redirect("catalog_detail")  # Only one catalog per vendor

    if request.method == "POST":
        form = CatalogForm(request.POST)
        if form.is_valid():
            catalog = form.save(commit=False)
            catalog.vendor = vendor
            catalog.save()
            form.save_m2m()
            return redirect("catalog_detail")
    else:
        form = CatalogForm()
    return render(request, "catalog/catalog_form.html", {"form": form})


@role_required("Vendor")
def catalog_update(request):
    catalog = get_object_or_404(Catalog, vendor=request.user.userprofile)
    if request.method == "POST":
        form = CatalogForm(request.POST, instance=catalog)
        if form.is_valid():
            form.save()
            return redirect("catalog_detail")
    else:
        form = CatalogForm(instance=catalog)
    return render(request, "catalog/catalog_form.html", {"form": form})


@role_required("Vendor")
def catalog_delete(request):
    catalog = get_object_or_404(Catalog, vendor=request.user.userprofile)
    if request.method == "POST":
        catalog.delete()
        return redirect("catalog_detail")
    return render(request, "catalog/catalog_confirm_delete.html", {"catalog": catalog})
