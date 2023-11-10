# Generated by Django 4.2.2 on 2023-10-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0026_livepresfeed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Termik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OvenName', models.CharField(null=True)),
                ('SampleTime', models.DateTimeField(null=True)),
                ('Bolge1', models.FloatField(null=True)),
                ('OrtaBolge', models.FloatField(null=True)),
                ('Bolge2', models.FloatField(null=True)),
                ('Bolge1TB', models.FloatField(null=True)),
                ('Bolge2TB', models.FloatField(null=True)),
                ('ProgramSet', models.CharField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='livepresfeed',
            name='Start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='livepresfeed',
            name='Stop',
            field=models.DateTimeField(null=True),
        ),
    ]