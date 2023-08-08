from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from device_transaction.models import Transaction
from device_transaction.serializers import DeviceTransactionSerializer


class DeviseTransactionViewsSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = DeviceTransactionSerializer
