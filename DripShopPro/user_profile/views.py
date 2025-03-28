from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile


def home(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role in ["Merchant", "Vendor"]:
                return redirect("dashboard")
        except:
            pass
    return render(request, "home.html")


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registration successful. Please wait for admin approval."
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "auth/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in.")
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.role in ["Merchant", "Vendor"]:
                        return redirect("dashboard")
                    else:
                        return redirect("home")
                except:
                    return redirect("home")

            else:
                messages.error(request, "Your account is not approved yet.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
