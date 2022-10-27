from django.db import models

# Create your models here.
class Recommend(models.Model):
    recommendNum = models.BigAutoField(verbose_name="추천상품번호", primary_key=True)
    userId = models.CharField(max_length=50 , verbose_name="아이디")
    prodList = models.CharField(verbose_name="추천 상품 리스트", max_length=150, null=True)
    status = models.CharField(verbose_name="추천상태", max_length=20)