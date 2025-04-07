from django import forms
from store.models import Store


class StoreForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter company name"}
        ),
        error_messages={"required": "Company name is required."},
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email address"}
        ),
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter phone number"}
        ),
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter address"}
        ),
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter city"}
        ),
    )

    state = forms.ChoiceField(
        choices=[("", "Select a state")] + Store.INDIAN_STATES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter postal code"}
        ),
    )

    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " mb-3"

    class Meta:
        model = Store
        fields = [
            "name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "postal_code",
            "logo",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        is_update = bool(self.instance and self.instance.pk)

        if is_update:
            if self.instance.name != name:
                if Store.objects.filter(name=name, is_deleted=False).exists():
                    raise forms.ValidationError(
                        "A store with this name already exists."
                    )
        else:
            if Store.objects.filter(name=name, is_deleted=False).exists():
                raise forms.ValidationError("A store with this name already exists.")

        return name
