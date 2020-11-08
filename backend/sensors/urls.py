from rest_framework.routers import DefaultRouter

from sensors.views import SensorViewSet

app_name = "sensors"

router = DefaultRouter()
router.register(r"sensors", SensorViewSet)

urlpatterns = router.urls
