from api.views import CompanyViewSet, MetaUserAPIView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)

urlpatterns = [
    path(r"auth/users/meta/", MetaUserAPIView.as_view(), name="user-meta"),
    path(r"auth/", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
]
