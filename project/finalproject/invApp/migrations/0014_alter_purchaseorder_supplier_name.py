# Generated by Django 5.1.4 on 2025-01-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invApp", "0013_alter_purchaseorder_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorder",
            name="supplier_name",
            field=models.CharField(max_length=100),
        ),
    ]
