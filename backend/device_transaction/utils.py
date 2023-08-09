from device_transaction.models import Transaction


def create_transaction(user, device, changed_fields: dict)-> None:
    Transaction(user=user, device)