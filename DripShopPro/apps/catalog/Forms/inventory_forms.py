from django import forms
from catalog.models import Inventory, Product, Company


class InventoryForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),  # Initially empty
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={"required": "Company is required."},
        empty_label="Select a Company",
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),  # Initially empty
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={"required": "Product is required."},
        empty_label="Select a Product",
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1.00,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter price"}
        ),
        error_messages={
            "required": "Price is required.",
            "min_value": "Price must be greater than 0.",
        },
    )

    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter stock quantity"}
        ),
        error_messages={"min_value": "Stock cannot be negative."},
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Extract `user` from kwargs
        super().__init__(*args, **kwargs)

        # Show only company and products created by the current vendor
        if self.user:
            self.fields["company"].queryset = Company.objects.filter(
                owner__user=self.user, is_deleted=False
            )
            self.fields["product"].queryset = Product.objects.filter(
                vendor__user=self.user,
                is_deleted=False,
            )

        # Apply consistent Bootstrap styling to all fields
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " mb-3"

    class Meta:
        model = Inventory
        fields = ["company", "product", "price", "stock"]

    def clean_product(self):
        product = self.cleaned_data.get("product")
        # Check if we're updating an existing product
        is_update = bool(self.instance and self.instance.pk)

        if is_update:
            if not self.instance.product == product:
                if Inventory.objects.filter(
                    product=product,
                    is_deleted=False,
                ).exists():
                    raise forms.ValidationError(
                        "You already have this Product in Inventory."
                    )
        else:
            if Inventory.objects.filter(
                product=product,
                is_deleted=False,
            ).exists():
                raise forms.ValidationError(
                    "You already have this Product in Inventory."
                )
        return product
