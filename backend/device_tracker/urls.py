from django.urls import path, include
from rest_framework import routers
from device_tracker import views
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
    path("api/", include(router.urls)),
    path("", views.home, name="home"),
    path("devices/<int:device_id>/", views.device_detail, name="device-detail"),
    path("devices/", views.devices, name="devices"),
]

app_name = "device_tracker"
