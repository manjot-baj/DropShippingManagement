from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


def register(request):
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

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("dashboard")
            else:
                messages.error(request, "Your account is not approved yet.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
