from django.contrib import admin
from cart.models import Cart

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ("cartNum", "userId", "prodNum", "buyCount")
admin.site.register(Cart, CartAdmin)