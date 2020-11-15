from rest_framework.routers import DefaultRouter
from sensors.views import SensorViewSet, SpeedRecordViewSet, HeadRotateRecordViewSet

app_name = "sensors"

router = DefaultRouter()
router.register(r"sensors", SensorViewSet)
router.register(r"speeds", SpeedRecordViewSet)
router.register(r"angle", HeadRotateRecordViewSet)

urlpatterns = router.urls
