from django.db import models

# Create your models here.
class Refund(models.Model):
    refundProdNum = models.BigAutoField(verbose_name="교환반품등록번호", primary_key=True)      #교환반품등록번호
    userId = models.CharField(max_length=50 , verbose_name="주문자 아이디", null=False)        #userId
    orderDetailNum = models.ForeignKey("order.OrderDetail", on_delete=models.CASCADE, db_column="orderDetailNum")#주문번호
    refund_exchangecheck = models.CharField(max_length=10 ,verbose_name="반품/교환선택" ) #반품 교환을 선택
    reason = models.TextField(verbose_name="반품/교환내용",null=False) #반품내용
    refundDate =models.DateTimeField(auto_now_add=True,verbose_name="작성일",blank=True)# 작성일
    status = models.CharField(verbose_name="반품/교환상태",max_length=1 , default="n")# 반품상태
    refundPhoto = models.ImageField(upload_to="refundphotos") #반품이미지
