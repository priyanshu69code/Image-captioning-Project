from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from .models import Product, SubscriptionLevel, History

admin.site.register(Product)
admin.site.register(SubscriptionLevel)
admin.site.register(History)
