# Generated by Django 2.1 on 2021-11-14 02:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartBook',
            new_name='exchange',
        ),
    ]
