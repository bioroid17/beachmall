from django.db import models

# Create your models here.
class Qnaboard( models.Model ) :
    qnaNum = models.AutoField( verbose_name="글번호", primary_key=True ) #
    userId = models.CharField( max_length=20, verbose_name="작성자", null=False ) #
    qnaTitle = models.CharField( max_length=1000, verbose_name="글제목", null=False ) #
    qnaContent = models.TextField( verbose_name="글내용", null=False ) #
    qnaScore = models.IntegerField( verbose_name="조회수", default=0, null=False ) #
    qnaDate = models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True, null=False ) #
    qnaIp = models.CharField( max_length=15, verbose_name="아이피", null=False )##
    reply_title= models.CharField( max_length=1000, verbose_name="댓글제목", null=True)#
    reply_content = models.TextField( verbose_name="관리자 댓글", null=True)