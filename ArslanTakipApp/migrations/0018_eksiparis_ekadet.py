# Generated by Django 4.2.2 on 2023-08-31 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0017_alter_eksiparis_ekdurumu'),
    ]

    operations = [
        migrations.AddField(
            model_name='eksiparis',
            name='EkAdet',
            field=models.IntegerField(null=True),
        ),
    ]