from django.conf.urls import url
from django.urls import include
from api.views import MetaUserAPIView

app_name = "api"


urlpatterns = [
    url(r"auth/users/meta/", MetaUserAPIView.as_view(), name="user-meta"),
    url(r"auth/", include("djoser.urls")),
    url(r"auth/", include("djoser.urls.jwt")),
]
