# Generated by Django 5.2 on 2025-05-15 07:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0003_booking_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="booking_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
