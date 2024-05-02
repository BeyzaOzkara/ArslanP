# Generated by Django 4.2.2 on 2024-05-02 14:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ArslanTakipApp', '0067_rename_made_by_notification_col_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ViewedUsers',
            field=models.ManyToManyField(blank=True, related_name='viewed_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]