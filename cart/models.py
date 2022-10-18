from django.db import models

# Create your models here.
class Cart(models.Model):
    cartNum = models.BigAutoField(verbose_name="장바구니 번호", primary_key=True)
    userId = models.ForeignKey("member.Member", on_delete=models.CASCADE, db_column="userId")
    prodNum = models.ForeignKey("product.Product", on_delete=models.CASCADE, db_column="prodNum")
    buyCount = models.IntegerField(verbose_name="선택한 상품의 수량", null=False)
    is_active = models.BooleanField(verbose_name="활성화 여부", null=False, default=True)