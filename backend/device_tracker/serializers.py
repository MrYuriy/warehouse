from rest_framework import serializers
from device_tracker.models import (
    Site,
    Department,
    Status,
    DeviceType,
    Port,
    IP,
    Device
)


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("department", "site")


class DepartmentListSerializer(DepartmentSerializer):
    site = serializers.SlugRelatedField(read_only=True, slug_field="site")


class DepartmentDetailSerializer(DepartmentSerializer):
    site = SiteSerializer(read_only=True)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = "__all__"


class IPListSerializer(IPSerializer):
    department = serializers.SlugRelatedField(read_only=True, slug_field="department")


class IPDetailSerializer(IPSerializer):
    department = DepartmentSerializer(read_only=True)


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = "__all__"


class PortListDeviceSerializer(PortSerializer):
    site = serializers.SlugRelatedField(read_only=True, slug_field="site")


class PortDetailDeviceSerializer(PortSerializer):
    site = SiteSerializer(read_only=True)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "device_type",
            "device_name",
            "device_serial_number",
            "device_status",
            "device_ip",
            "device_ports",
            "department",
        )

    def validate(self, data):
        ports = data.get("device_ports")
        ip = data.get("device_ip")
        if not ports or not ip:
            raise serializers.ValidationError("Device mast to have IP or Port")
        return data


class DeviceListSerializer(DeviceSerializer):
    device_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="device_type"
    )
    device_status = serializers.SlugRelatedField(
        read_only=True,
        slug_field="status"
    )
    department = serializers.SlugRelatedField(
        read_only=True,
        slug_field="department"
    )
    device_ports = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="port"
    )
    device_ip = serializers.SlugRelatedField(
        read_only=True,
        slug_field="ip"
    )


class DeviceDetailSerializer(DeviceSerializer):
    device_type = DeviceTypeSerializer(read_only=True)
    device_status = StatusSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    device_ports = PortListDeviceSerializer(read_only=True, many=True)
    device_ip = IPSerializer(many=True, read_only=True)
