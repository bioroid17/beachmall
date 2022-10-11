from django.db import models

# Create your models here.
class Order(models.Model):
    orderNum = models.BigAutoField(verbose_name="주문번호", primary_key=True)
    userId = models.CharField(max_length=50 , verbose_name="주문자 아이디", null=False)
    getterName = models.CharField(max_length=50 , verbose_name="받는 사람 이름", null=False)
    getterAddress = models.CharField(max_length=500 , verbose_name="받는 사람 주소", null=False)
    getterDetailAddr = models.CharField(max_length=500 , verbose_name="받는 사람 상세주소", null=False)
    getterZonecode = models.CharField(max_length=10 , verbose_name="받는 사람 우편번호", null=False)
    getterTel = models.CharField(max_length=20, verbose_name="받는 사람 전화번호", null=False)
    requirement = models.TextField(verbose_name="요구사항", null=True)
    orderMsg = models.TextField(verbose_name="주문 메세지", null=True)
    totalPrice = models.BigIntegerField(verbose_name="총액", null=False)
    orderDate = models.DateTimeField(auto_now_add=True, verbose_name="주문날짜", null=False, blank=True)
    
class OrderDetail(models.Model):
    orderDetailNum = models.BigAutoField(verbose_name="주문상세번호", primary_key=True)
    orderNum = models.ForeignKey("Order", on_delete=models.CASCADE, db_column="orderNum")
    prodNum = models.BigIntegerField(verbose_name="상품번호", null=False)
    prodName = models.CharField(verbose_name="상품명", null=False, max_length=1000)
    prodThumbnail = models.CharField(verbose_name="썸네일", null=False, max_length=1000)
    prodPrice = models.BigIntegerField(verbose_name="상품 가격", null=False)
    buyCount = models.IntegerField(verbose_name="구매 수량", null=False)
    prodTotal = models.IntegerField(verbose_name="구매 금액", null=False)
    is_refunded = models.BooleanField(verbose_name="반품/환불/교환 여부", default=0)