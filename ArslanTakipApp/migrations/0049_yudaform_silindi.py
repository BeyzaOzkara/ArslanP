# Generated by Django 4.2.2 on 2024-03-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0048_remove_yudaonay_kullanici_yudaonay_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='yudaform',
            name='Silindi',
            field=models.BooleanField(null=True),
        ),
    ]