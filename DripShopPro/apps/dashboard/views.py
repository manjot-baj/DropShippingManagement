from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_profile.models import UserProfile


@login_required
def dashboard(request):
    user = UserProfile.objects.get(user=request.user)
    return render(request, f"{user.role.lower()}/dashboard.html", {"user": user})
