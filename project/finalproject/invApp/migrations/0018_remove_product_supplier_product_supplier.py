# Generated by Django 5.1.4 on 2025-01-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invApp", "0017_rename_description_supplier_supplies_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="supplier",
        ),
        migrations.AddField(
            model_name="product",
            name="supplier",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]