from django import forms
from order.models import Order


class OrderForm(forms.ModelForm):

    address = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter address"}
        ),
        error_messages={"required": "Address name is required."},
    )

    city = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter city"}
        ),
        error_messages={"required": "City name is required."},
    )

    state = forms.ChoiceField(
        choices=[("", "Select a state")] + Order.INDIAN_STATES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={"required": "State name is required."},
    )

    postal_code = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter postal code"}
        ),
        error_messages={"required": "Postal Code name is required."},
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " mb-3"

    class Meta:
        model = Order
        fields = [
            "address",
            "city",
            "state",
            "postal_code",
        ]
