from django.shortcuts import render


def index(request):
    return render(request, "django_sp_admin/index.html")
