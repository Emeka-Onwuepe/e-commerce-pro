from django.contrib import admin
from .models import Bad_Product, Category, Product, Product_Type, Returned_Product, Size

# Register your models here.
admin.site.register(Category)
admin.site.register(Product_Type)
admin.site.register(Product)
admin.site.register(Bad_Product)
admin.site.register(Returned_Product)
admin.site.register(Size)




