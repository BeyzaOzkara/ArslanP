# Generated by Django 4.2.2 on 2023-08-03 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StokApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HareketTuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='Hareket Türü')),
            ],
        ),
        migrations.AlterField(
            model_name='stockcard',
            name='PackageUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_unit', to='StokApp.unit', verbose_name='Ambalaj Birimi'),
        ),
        migrations.CreateModel(
            name='SLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', models.CharField(max_length=255, verbose_name='Lokasyon İsmi')),
                ('locationRelationID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StokApp.slocation')),
            ],
        ),
        migrations.CreateModel(
            name='SHareket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Miktar', models.DecimalField(decimal_places=3, max_digits=255, null=True, verbose_name='Miktar')),
                ('hareketTarihi', models.DateTimeField(auto_now=True, null=True)),
                ('StokNo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='StokApp.stockcard', verbose_name='Stok Kodu')),
                ('byWhom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Kim Tarafından')),
                ('fromLocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_location', to='StokApp.slocation', verbose_name='Nereden')),
                ('toLocation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_location', to='StokApp.slocation', verbose_name='Nereye')),
            ],
        ),
    ]