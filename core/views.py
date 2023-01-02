from django.shortcuts import render, redirect


def homepage(request):
    if request.user.is_authenticated:
        return redirect("highlights:list")
    return render(request, "core/home.html")
