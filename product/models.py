from django.db import models
from product.choice import BRAND_CHOICE

# Create your models here.
class Product(models.Model):
    prodNum = models.BigAutoField(verbose_name="상품번호", primary_key=True)
    prodName = models.CharField(verbose_name="상품명", null=False, max_length=1000)
    prodStock = models.IntegerField(verbose_name="재고", null=False)
    prodPrice = models.BigIntegerField(verbose_name="가격", null=False)
    prodInfo = models.TextField(verbose_name="상품 설명", null=False, max_length=30000)
    prodThumbnail = models.ImageField(verbose_name="썸네일", null=False, upload_to="products")
    prodImage1 = models.ImageField(verbose_name="이미지1", null=False, upload_to="products")
    prodImage2 = models.ImageField(verbose_name="이미지2", null=False, upload_to="products")
    searchCount = models.BigIntegerField(verbose_name="조회수", null=False)
    status = models.SmallIntegerField(verbose_name="상태", null=False)
    brand = models.CharField(verbose_name="브랜드", null=False, max_length=100, choices=BRAND_CHOICE)