from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


@login_required
def profile_update(request):
    """Редактирование профиля"""
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "account/profile.html", {"form": form})
