from django.urls import include, path

urlpatterns = [
    path("bread/", include("bread.urls")),
    path("basxconnect/", include("basxconnect.core.urls")),
]
