from django.db import models
from users.models import User
import os, datetime


def set_filename_format(now, instance, filename):
    return "{exchange_type}-{date}-{microsecond}{extension}".format(
        exchange_type=instance.exchange_type,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def exchange_directory_path(instance, filename):
    now = datetime.datetime.now()
    path = "exchange/image/{exchange_type}/{filename}".format(
        exchange_type=instance.exchange_type,
        filename=set_filename_format(now, instance, filename),
    )
    return path


# Create your models here.
class Exchange(models.Model):
    exchange_type = models.CharField(max_length=10, blank=False)
    exchange_image = models.FileField(upload_to=exchange_directory_path, null=False, default="")
    # exchange_image = models.FileField()

    class Meta:
        db_table = 'exchange'


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
