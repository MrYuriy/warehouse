from django.db import models
from warehouse import settings
from device_tracker.models import Device


class Transaction(models.Model):
    transaction_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return f"{self.notes}"
