from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="django_sp_admin"),
]
