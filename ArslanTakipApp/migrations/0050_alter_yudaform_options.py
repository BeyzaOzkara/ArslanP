# Generated by Django 4.2.2 on 2024-03-22 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0049_yudaform_silindi'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yudaform',
            options={'permissions': [('gorme_yuda', 'Yuda Gorme Yetkisi Var'), ('yonetici_yuda', 'Yuda Proje Yoneticisi')], 'verbose_name': 'YudaForm', 'verbose_name_plural': 'YudaForms'},
        ),
    ]
