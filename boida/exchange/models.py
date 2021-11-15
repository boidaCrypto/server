from django.db import models
from users.models import User


# Create your models here.

class Exchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exchange_type = models.CharField(max_length=10, blank=False)
    access_key = models.TextField(default='')
    secret_key = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'exchange'


class Upbit(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.SET_NULL, null=True)
    uuid = models.CharField(max_length=40, null=False, default="")
    side = models.CharField(max_length=3, null=False, default="")
    order_type = models.CharField(max_length=7, null=False, default="")
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
    trade_count = models.IntegerField()
    created_at = models.DateTimeField()
