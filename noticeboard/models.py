from django.db import models

# Create your models here.
class NoticeBoard(models.Model):
                        #admin에서 보여주는것
    noticeNum = models.AutoField(verbose_name="글번호", primary_key=True) #자동증가
    admin = models.CharField(max_length=30, verbose_name="작성자", null=False)
    noticeTitle = models.CharField(max_length=1000, verbose_name="글제목", null=False) 
    noticeContent = models.TextField(verbose_name="글내용", null=False) 
    noticeDate = models.DateTimeField(auto_now_add=True,verbose_name="작성일",blank=True)
    
    def __str__(self):
        return self.noticeTitle