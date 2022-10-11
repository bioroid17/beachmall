from django.contrib import admin
from product.models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("prodNum", "prodName", "prodStock", "prodPrice", "prodInfo", "prodThumbnail",
                    "prodImage1", "prodImage2", "searchCount", "status", "brand")
admin.site.register(Product, ProductAdmin)