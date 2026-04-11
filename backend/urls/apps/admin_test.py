from django.urls import include, path


urlpatterns = [
    path("admin_test/", include("admin_test.urls")),
]
