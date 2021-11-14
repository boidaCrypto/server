from django.db import models
from users.models import User


# Create your models here.

class exchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exchange_type = models.CharField(max_length=10, blank=False)
    api_key = models.TextField(default='')
    secret_key = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
