from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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
    IPDetailSerializer,
    IPListSerializer,
    PortSerializer,
    PortListDeviceSerializer,
    PortDetailDeviceSerializer,
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

    def get_serializer_class(self):
        if self.action == "list":
            return IPListSerializer
        if self.action == "retrieve":
            return IPDetailSerializer
        return IPSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.GET.get("department")
        site = self.request.GET.get("site")

        if site:
            queryset = queryset.filter(department__site__site=site)
        if department:
            queryset = queryset.filter(department__department=department)
        return queryset


class PortViewSet(ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PortListDeviceSerializer
        if self.action == "retrieve":
            return PortDetailDeviceSerializer
        return PortSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        site = self.request.GET.get("site")
        if site:
            queryset = queryset.filter(site__site=site)
        return queryset


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    permission_classes = (IsAuthenticated, )

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
        site = self.request.GET.get("site")
        status = self.request.GET.get("status")

        if site:
            queryset = queryset.filter(department__site__site=site)
        if status:
            queryset = queryset.filter(device_status__status=status)

        return queryset
