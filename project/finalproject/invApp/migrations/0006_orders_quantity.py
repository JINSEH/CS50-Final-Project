# Generated by Django 5.1.4 on 2025-01-06 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invApp", "0005_orders_products"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
