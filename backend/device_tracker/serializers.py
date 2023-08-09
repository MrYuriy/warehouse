from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404
from device_transaction.utils import create_transaction

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

    def update(self, instance, validated_data):
        instance.site = validated_data.get("site", instance.site)
        instance.port = validated_data.get("port", instance.port)
        instance.save()
        return instance


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
        if not ports and not ip:
            raise serializers.ValidationError("Device mast to have IP or Port")
        return data

    def update(self, instance, validated_data):
        request = self.context.get("request")

        new_serial_number = validated_data.get("device_serial_number", None)
        # changed_fields - dictionary for transaction that contain fields what was change
        changed_fields = {}
        for attr, value in validated_data.items():
            if attr == 'device_ports':
                old_ports = set(instance.device_ports.all())
                new_ports = set(value)
                if old_ports != new_ports:
                    changed_fields[attr] = {
                        "old_value": [port.port for port in old_ports],
                        "new_value": [port.port for port in new_ports]
                    }

            else:
                if getattr(instance, attr) != value:
                    changed_fields[attr] = {"old_value": str(getattr(instance, attr)), "new_value": str(value)}

        # if user change serial number its meat changing physical device
        if instance.device_serial_number not in [None, new_serial_number]:

            with transaction.atomic():
                new_devise = Device(
                    device_type=validated_data.get("device_type", instance.device_type),
                    device_name=validated_data.get("device_name", instance.device_name),
                    device_serial_number=new_serial_number,
                    device_status=get_object_or_404(Status, status="WORK"),
                    device_ip=validated_data.get("device_ip", instance.device_ip),
                    department=validated_data.get("department", instance.department)
                )
                new_devise.save()
                new_devise.device_ports.set(validated_data.get("device_ports", instance.device_ports))

                instance.device_status = get_object_or_404(Status, status="REPLACED")
                instance.device_ports.set([])
                instance.save()
                instance = new_devise
        else:
            instance.device_type = validated_data.get("device_type", instance.device_type)
            instance.device_name = validated_data.get("device_name", instance.device_name)
            instance.device_serial_number = validated_data.get("device_serial_number", instance.device_serial_number)
            instance.device_status = validated_data.get("device_status", instance.device_status)
            instance.device_ip = validated_data.get("device_ip", instance.device_ip)
            instance.device_ports.set(validated_data.get("device_ports", instance.device_ports.all()))
            instance.department = validated_data.get("department", instance.department)
            instance.save()
        create_transaction(user=request.user, device=instance, changed_fields=changed_fields)
        return instance


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
