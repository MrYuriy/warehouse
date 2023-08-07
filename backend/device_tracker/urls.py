from django.urls import path, include
from rest_framework import routers
from device_tracker.views import (
    DeviceViewSet,
    PortViewSet,
    SiteViewSet,
    IPViewSet,
    DeviceTypeViewSet,
    DepartmentViewSet,
    StatusViewSet,
    DeviceStatusViewSet,
)

router = routers.DefaultRouter()
router.register("device", DeviceViewSet)
router.register(r"port", PortViewSet)
router.register(r"site", SiteViewSet)
router.register(r"ip", IPViewSet)
router.register(r"device-type", DeviceTypeViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"device-status", DeviceStatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "device_tracker"
