# Generated by Django 2.1 on 2021-11-15 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_remove_upbit_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='upbit',
            name='exchange',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange.Exchange'),
        ),
    ]