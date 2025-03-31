import logging
import traceback
from django import forms
from catalog.models import Product, Category

logger = logging.getLogger("error_log")  # Centralized logger


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={"required": "Product name is required."},
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), required=False
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # Initially empty
        required=True,
        error_messages={"required": "Category is required."},
        empty_label="Select a category",
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        error_messages={
            "required": "Price is required.",
            "min_value": "Price must be greater than 0.",
        },
    )

    stock = forms.IntegerField(
        min_value=0, error_messages={"min_value": "Stock cannot be negative."}
    )

    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs.pop("user", None)  # Extract `user` from kwargs
            super().__init__(*args, **kwargs)

            # Show only categories created by the current vendor
            if self.user:
                self.fields["category"].queryset = Category.objects.filter(
                    vendor__user=self.user
                )
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "stock"]

    def clean_name(self):
        try:
            name = self.cleaned_data.get("name")
            if Product.objects.filter(
                name__iexact=name, vendor__user=self.user
            ).exists():
                raise forms.ValidationError(
                    "A product with this name already exists in your store."
                )
            return name
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def clean_category(self):
        try:
            category = self.cleaned_data.get("category")
            if (
                category
                and Category.objects.filter(
                    name__iexact=category.name, vendor__user=self.user
                ).exists()
            ):
                raise forms.ValidationError(
                    "A category with this name already exists for your store."
                )
            return category
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def clean_price(self):
        try:
            price = self.cleaned_data.get("price")
            if price and price > 99999:
                raise forms.ValidationError("Price must not exceed Rs.99999/-")
            return price
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
