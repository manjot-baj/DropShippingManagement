from django import forms
from catalog.models import Product, Category


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter product name"}
        ),
        error_messages={"required": "Product name is required."},
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Enter description (optional)",
            }
        ),
        required=False,
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # Initially empty
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={"required": "Category is required."},
        empty_label="Select a category",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Extract `user` from kwargs
        super().__init__(*args, **kwargs)

        # Show only all categories
        if self.user:
            self.fields["category"].queryset = Category.objects.all()

        # Apply consistent Bootstrap styling to all fields
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " mb-3"

    class Meta:
        model = Product
        fields = ["name", "description", "category"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Check if we're updating an existing product
        is_update = bool(self.instance and self.instance.pk)

        if is_update:
            if not self.instance.name == name:
                if Product.objects.filter(
                    name=name,
                    vendor__user=self.user,
                    is_deleted=False,
                ).exists():
                    raise forms.ValidationError(
                        "You already have a Product with this name. Please use a unique name."
                    )
        else:
            if Product.objects.filter(
                name=name,
                vendor__user=self.user,
                is_deleted=False,
            ).exists():
                raise forms.ValidationError(
                    "You already have a Product with this name. Please use a unique name."
                )
        return name
