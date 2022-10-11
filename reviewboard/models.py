from django.db import models

# Create your models here.    
class Reviewboard(models.Model):
    reviewNum = models.AutoField( verbose_name="글번호", primary_key=True)
    prodNum = models.ForeignKey( "product.Product", on_delete=models.CASCADE, db_column="prodNum")
    userId = models.CharField( max_length=20, verbose_name="작성자", null=False )
    reviewDate = models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True, null=False )
    reviewTitle = models.CharField( max_length=1000, verbose_name="글제목", null=False )
    reviewContent = models.TextField( verbose_name="글내용", null=False )
    reviewIp = models.CharField( max_length=15, verbose_name="아이피", null=False )
    reviewPhoto = models.ImageField( upload_to="reviews", null=True )
