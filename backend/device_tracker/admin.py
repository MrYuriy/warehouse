from django.contrib import admin
from .models import Status, DeviceType, Port, Device, Site, Department, IP
from django import forms


class MyDeviceAdminForm(forms.ModelForm):
    """
    custom form for checked reserved ports
    """
    def clean_ports(self):
        cleaned_ports = [port.port for port in self.cleaned_data.get("ports")]
        existing_device = Device.objects.prefetch_related("ports").all()
        port_reserved_list = []

        for device in existing_device:
            port_reserved_list += [
                port.port for port in device.ports.all() if port.port in cleaned_ports
            ]
        if port_reserved_list:
            raise forms.ValidationError(
                f"Ports: {list(set(port_reserved_list))} already use"
            )

        return self.cleaned_data.get("ports")


class PortAdmin(admin.ModelAdmin):
    list_display = ("port",)
    search_fields = ("port",)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "get_ports", "ip")
    form = MyDeviceAdminForm

    def get_ports(self, obj):
        return ", ".join([str(port.port) for port in obj.ports.all()])
    get_ports.short_description = "Ports"
    filter_horizontal = ("ports",)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Status)
admin.site.register(DeviceType)
admin.site.register(Site)
admin.site.register(Department)
admin.site.register(IP)
