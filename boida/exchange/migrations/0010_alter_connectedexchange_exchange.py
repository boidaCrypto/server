# Generated by Django 3.2.9 on 2021-12-26 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_connectedexchange_is_sync'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectedexchange',
            name='exchange',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exchange', to='exchange.exchange'),
        ),
    ]