# Generated by Django 4.2.3 on 2023-08-04 03:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("device_tracker", "0003_rename_device_ports_device_ports"),
    ]

    operations = [
        migrations.RenameField(
            model_name="device",
            old_name="ports",
            new_name="device_ports",
        ),
    ]
