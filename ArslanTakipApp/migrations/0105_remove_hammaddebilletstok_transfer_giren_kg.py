# Generated by Django 4.2.2 on 2024-10-30 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0104_hammaddebillet_hammaddebilletstok_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hammaddebilletstok',
            name='transfer_giren_kg',
        ),
    ]