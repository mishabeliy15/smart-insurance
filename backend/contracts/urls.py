from contracts.views import ContractViewSet, OfferViewSet
from rest_framework.routers import DefaultRouter

app_name = "contracts"

router = DefaultRouter()
router.register(r"contracts", ContractViewSet)
router.register(r"offers", OfferViewSet)

urlpatterns = router.urls
