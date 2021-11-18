from django.db import models
from users.models import User
import os, datetime

LOCATION_CHOICES = (
    ('domestic', 'Domestic'),
    ('aboard', 'Aboard')
)


def set_filename_format(now, instance, filename):
    return "{exchange_name}-{date}-{microsecond}{extension}".format(
        exchange_name=instance.exchange_name,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def exchange_directory_path(instance, filename):
    now = datetime.datetime.now()
    path = "exchange/image/{exchange_name}/logo/{filename}".format(
        exchange_name=instance.exchange_name,
        filename=set_filename_format(now, instance, filename),
    )
    return path


def exchange_description_set_filename_format(now, filename):
    return "{date}-{microsecond}{extension}".format(
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def exchange_description_directory_path(instance, filename):
    now = datetime.datetime.now()
    exchange_name = instance.exchange.exchange_name
    path = "exchange/image/{exchange_name}/explain/{filename}".format(
        exchange_name=exchange_name,
        filename=exchange_description_set_filename_format(now, filename)
    )
    return path


# Create your models here.
class Exchange(models.Model):
    exchange_name = models.CharField(max_length=10, blank=False)
    exchange_image = models.FileField(upload_to=exchange_directory_path, null=False, default="")
    location = models.CharField(max_length=8, choices=LOCATION_CHOICES)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchange'

    def __str__(self):
        return self.exchange_name


class ConnectedExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.SET_NULL, null=True)
    access_key = models.TextField(default='')
    secret_key = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'connected_exchange'


class Transaction(models.Model):
    connected_exchange = models.ForeignKey(ConnectedExchange, on_delete=models.SET_NULL, null=True)
    uuid = models.CharField(max_length=40, null=False, default="")
    side = models.CharField(max_length=3, null=False, default="")
    ord_type = models.CharField(max_length=7, null=False, default="")
    price = models.FloatField()
    state = models.CharField(max_length=5, null=False, default="")
    market = models.CharField(max_length=20, null=False, default="")
    volume = models.FloatField()
    remaining_volume = models.FloatField()
    reserved_fee = models.FloatField()
    remaining_fee = models.FloatField()
    paid_fee = models.FloatField()
    locked = models.FloatField()
    executed_volume = models.FloatField()
    trades_count = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'transaction'


class ExchangeDescription(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.SET_NULL, null=True)
    description = models.TextField(default="")
    image = models.ImageField(upload_to=exchange_description_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'exchange_description'