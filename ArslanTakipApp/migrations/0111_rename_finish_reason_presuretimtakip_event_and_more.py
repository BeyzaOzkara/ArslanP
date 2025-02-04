# Generated by Django 4.2.2 on 2024-11-05 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0110_locationdies'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presuretimtakip',
            old_name='finish_reason',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='presuretimtakip',
            name='billet_boy_adet',
        ),
        migrations.RemoveField(
            model_name='presuretimtakip',
            name='destination',
        ),
        migrations.AddField(
            model_name='hammaddebilletcubuk',
            name='pres_uretim_takip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ArslanTakipApp.presuretimtakip'),
        ),
        migrations.AddField(
            model_name='presuretimtakip',
            name='reason',
            field=models.CharField(blank=True, null=True),
        ),
    ]
