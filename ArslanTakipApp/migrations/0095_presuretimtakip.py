# Generated by Django 4.2.2 on 2024-09-24 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0094_rename_sipkartno_eksiparis_kartno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresUretimTakip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siparis_kimlik', models.IntegerField(blank=True, null=True)),
                ('kalip_no', models.CharField(blank=True, null=True)),
                ('baslangic_datetime', models.DateTimeField(blank=True, null=True)),
                ('bitis_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'PresUretimTakip',
                'verbose_name_plural': 'PresUretimTakipler',
            },
        ),
    ]