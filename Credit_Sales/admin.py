from django.contrib import admin

from .models import Credit_Sale, Payment

# Register your models here.
admin.site.register(Credit_Sale)
admin.site.register(Payment)