# Generated by Django 4.2.2 on 2023-11-02 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArslanTakipApp', '0031_yuda_yuklenendosyalar_alter_yuda_bariyerleme_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='aciklama',
            new_name='Aciklama',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='eklenenDosyalar',
            new_name='EklenenDosyalar',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='form',
            new_name='Form',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='kullanici',
            new_name='Kullanici',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='tarih',
            new_name='Tarih',
        ),
        migrations.RenameField(
            model_name='yuda',
            old_name='yuklenenDosyalar',
            new_name='YuklenenDosyalar',
        ),
    ]