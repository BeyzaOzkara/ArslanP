# Generated by Django 4.2.2 on 2023-09-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0024_alter_location_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='capacity',
            field=models.IntegerField(null=True),
        ),
    ]