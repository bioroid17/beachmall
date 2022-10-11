from django.db import models

# Create your models here.
class Recommend(models.Model):
    recommendNum = models.BigAutoField(verbose_name="추천상품번호", primary_key=True)
    prodNum = models.ForeignKey("product.Product",on_delete=models.CASCADE, db_column="prodnum") #이거만 있으면됨 나중에 FK키
    status = models.CharField(verbose_name="추천상태", max_length=1)