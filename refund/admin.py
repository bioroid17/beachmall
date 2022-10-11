from django.contrib import admin
from refund.models import Refund

# Register your models here.
class RefundAdmin (admin.ModelAdmin):
                #컬럼이름을 줘야한다.
    list_display=("refundProdNum", "orderDetailNum", "refund_exchangecheck",
                  "reason", "refundDate", "status")
    
admin.site.register(Refund, RefundAdmin)