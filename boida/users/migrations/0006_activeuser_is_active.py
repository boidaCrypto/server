# Generated by Django 3.2.9 on 2021-12-30 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_activeuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]