from django.db import models
from users.models import User
# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.SET_NULL, null=True)
    target_user = models.ForeignKey(User,related_name='target_user', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, default='')
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)