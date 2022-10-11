from django.contrib import admin
from order.models import Order, OrderDetail

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ("orderNum", "userId", "getterName", "getterAddress", "getterDetailAddr",
                    "getterZonecode", "getterTel", "requirement", "orderMsg", "totalPrice", "orderDate")
admin.site.register(Order, OrderAdmin)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("orderDetailNum", "orderNum", "prodNum", "prodName", "prodPrice", "buyCount", "prodTotal")
admin.site.register(OrderDetail, OrderDetailAdmin)