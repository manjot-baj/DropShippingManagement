from django import forms
from catalog.models import Product, Catalog


class CatalogForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Catalog
        fields = ["title", "description", "products", "is_active"]
