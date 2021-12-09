# Generated by Django 3.2.9 on 2021-12-09 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import exchange.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0007_exchange_exchange_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crypto_name', models.CharField(default='', max_length=10)),
                ('image', models.ImageField(upload_to=exchange.models.crypto_description_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'crypto',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_amount', models.FloatField()),
                ('valuation_amount', models.FloatField()),
                ('valuation_loss', models.FloatField()),
                ('valuation_earning_rate', models.FloatField()),
                ('balance', models.FloatField()),
                ('crypto_ratio', models.FloatField(default=0)),
                ('crypto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange.crypto')),
                ('exchange', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange.exchange')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'asset',
            },
        ),
    ]
