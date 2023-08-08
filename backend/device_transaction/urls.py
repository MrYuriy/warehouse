from django.urls import path, include
from rest_framework import routers
from device_transaction.views import DeviseTransactionViewsSet


router = routers.DefaultRouter()
router.register("device-transaction", DeviseTransactionViewsSet)
urlpatterns = [
    path("", include(router.urls))
]

app_name = "device_transaction"
