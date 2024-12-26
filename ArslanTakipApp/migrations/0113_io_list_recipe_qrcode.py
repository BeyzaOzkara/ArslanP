# Generated by Django 4.2.2 on 2024-12-24 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0112_remove_hammaddebilletcubuk_pres_uretim_takip_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IO_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.CharField(blank=True, max_length=250, null=True)),
                ('unit', models.CharField(blank=True, max_length=250, null=True)),
                ('ip', models.CharField(blank=True, max_length=250, null=True)),
                ('label', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('protocol', models.CharField(blank=True, max_length=250, null=True)),
                ('writable', models.BooleanField(blank=True, null=True)),
                ('frequency', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'IO_List',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('profile_number', models.CharField(blank=True, max_length=250, null=True)),
                ('parameters', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Recipe',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr', models.CharField(blank=True, null=True)),
                ('name', models.CharField(blank=True, null=True)),
                ('detail', models.CharField(blank=True, null=True)),
            ],
        ),
    ]
