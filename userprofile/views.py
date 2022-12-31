from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

from . import models


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            models.UserProfile.objects.create(user=user)
            return redirect("userprofile:login")
        else:
            errors = form.errors.as_data()
            print(errors)
            for error in errors:
                problems = [str(problem) for problem in errors[error]]
                m = ",".join(problems)
                print("m", m)
                messages.add_message(request, messages.INFO, f"{error}: {m}")

    form = UserCreationForm()
    return render(request, "userprofile/signup.html", {"form": form})
