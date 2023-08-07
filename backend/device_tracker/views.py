from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from device_tracker.models import (
    Site,
    Department,
    Status,
    DeviceType,
    IP,
    Port,
    Device,
    Status,
)
from device_tracker.serializers import (
    SiteSerializer,
    DepartmentSerializer,
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    StatusSerializer,
    DeviceTypeSerializer,
    IPSerializer,
    PortSerializer,
    PortListDeviceSerializer,
    DeviceListSerializer,
    DeviceDetailSerializer,
    DeviceSerializer,
)


class DeviceStatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class DeviceTypeViewSet(ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class SiteViewSet(ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return DepartmentListSerializer
        if self.action == "retrieve":
            return DepartmentDetailSerializer
        return DepartmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        site = self.request.GET.get("site")
        if site:
            queryset = queryset.filter(site__site=site)
        return queryset


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class IPViewSet(ModelViewSet):
    queryset = IP.objects.all()
    serializer_class = IPSerializer


class PortViewSet(ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return DeviceListSerializer
        if self.action == "retrieve":
            return DeviceDetailSerializer
        return DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.select_related(
            "device_type", "device_status", "device_ip", "department"
        ).prefetch_related("device_ports")
        return queryset
