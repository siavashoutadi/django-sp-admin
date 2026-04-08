from django.urls import include, path


urlpatterns = [
    path("django_sp_admin/", include("django_sp_admin.urls")),
]
