from rest_framework import serializers
from device_transaction.models import Transaction


class DeviceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
