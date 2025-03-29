from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    username = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    mobile_no = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "role",
            "username",
            "email",
            "mobile_no",
            "password",
            "confirm_password",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get("mobile_no")
        if not mobile_no.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if UserProfile.objects.filter(mobile_no=mobile_no).exists():
            raise forms.ValidationError(
                "This mobile_no is already registered with other user."
            )
        return mobile_no

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email_id=email).exists():
            raise forms.ValidationError(
                "This email is already registered with other user."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """Override save to create a linked User object and ensure password hashing."""
        if not self.is_valid():
            raise ValueError("Cannot save user: form is not valid.")

        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password"])  # Hash password before saving
        if commit:
            user.save()

            # Create and save the UserProfile instance
            user_profile = UserProfile(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
                role=self.cleaned_data["role"],
                mobile_no=self.cleaned_data["mobile_no"],
                email_id=self.cleaned_data["email"],
                is_approved=self.cleaned_data["role"]
                == "Customer",  # Auto-approve customers
            )
        if commit:
            user_profile.save()

        return user_profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
