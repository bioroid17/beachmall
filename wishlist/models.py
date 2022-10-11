from django.db import models

# Create your models here.
class Wishlist(models.Model):
    wishNum = models.BigAutoField(verbose_name="장바구니 번호", primary_key=True)
    userId = models.ForeignKey("member.Member", on_delete=models.CASCADE, db_column="userId")
    prodNum = models.ForeignKey("product.Product", on_delete=models.CASCADE, db_column="prodNum")