from django.db import models


class Site(models.Model):
    """
    like EMAG 445 493 9999
    """
    site = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Site {self.site}"


class Department(models.Model):
    """
    like: Site + department name
    """
    department = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["department", "site"], name="unique_department")
        ]

    def __str__(self):
        return f"{self.department}"


class Status(models.Model):
    """
    like: warehouse ,service ...
    """

    status = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Devise status"
        verbose_name_plural = "Devises status"

    def __str__(self):
        return f"{self.status}"


class DeviceType(models.Model):
    """
    like: barcode scaner, mobile printer ...
    """

    device_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.device_type}"


class Port(models.Model):
    """
    ports for barcode scaner
    """

    port = models.IntegerField(unique=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.port} - {self.site}"


class IP(models.Model):
    """
    IP for printers
    """
    ip = models.GenericIPAddressField(blank=True, null=True, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"IP: {self.ip}"


class Device(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=255)
    device_serial_number = models.CharField(max_length=255, unique=True)
    device_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    device_ip = models.ForeignKey(IP, blank=True, null=True, on_delete=models.SET_NULL)
    device_ports = models.ManyToManyField(Port, related_name="devices", blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="devices")

    def __str__(self):
        return f"{self.device_type} {self.device_name}: {self.device_serial_number}"
