from rest_framework.routers import DefaultRouter
from sensors.views import SensorViewSet, SpeedRecordViewSet

app_name = "sensors"

router = DefaultRouter()
router.register(r"sensors", SensorViewSet)
router.register(r"speeds", SpeedRecordViewSet)

urlpatterns = router.urls
