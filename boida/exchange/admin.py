from django.contrib import admin
from exchange.models import Exchange, ExchangeDescription
# Register your models here.
admin.site.register(Exchange)
admin.site.register(ExchangeDescription)