from django.urls import include, path

urlpatterns = [
    path("basxbread/", include("basxbread.urls")),
    path("basxconnect/", include("basxconnect.core.urls")),
]
