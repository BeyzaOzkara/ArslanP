# Generated by Django 4.2.2 on 2024-08-03 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0093_rename_ekadet_eksiparis_adet_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eksiparis',
            old_name='SipKartNo',
            new_name='KartNo',
        ),
        migrations.RenameField(
            model_name='eksiparis',
            old_name='SipKimlik',
            new_name='Kimlik',
        ),
    ]