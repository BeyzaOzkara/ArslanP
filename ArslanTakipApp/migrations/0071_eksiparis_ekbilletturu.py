# Generated by Django 4.2.2 on 2024-05-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0070_alter_yudaonay_yuda'),
    ]

    operations = [
        migrations.AddField(
            model_name='eksiparis',
            name='EkBilletTuru',
            field=models.CharField(blank=True, null=True),
        ),
    ]