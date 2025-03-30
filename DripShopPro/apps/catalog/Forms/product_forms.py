from django import forms
from catalog.models import Product, Category


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
        required=False,
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

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Extract `user` from kwargs
        super().__init__(*args, **kwargs)

        # Show only categories created by the current vendor
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(
                vendor__user=self.user
            )

    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "stock"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Product.objects.filter(name__iexact=name, vendor__user=self.user).exists():
            raise forms.ValidationError(
                "A product with this name already exists in your store."
            )
        return name

    def clean_category(self):
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

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price and price > 99999:
            raise forms.ValidationError("Price must not exceed Rs.99999/-")
        return price

    def clean_images(self):
        images = self.files.getlist("images")  # Ensure multiple images can be uploaded
        for image in images:
            if image.size > 5 * 1024 * 1024:  # Limit image size to 5MB
                raise forms.ValidationError("Each image must be less than 5MB.")
            if not image.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise forms.ValidationError("Only JPG and PNG images are allowed.")
        return images
