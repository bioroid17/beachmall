from django.db import models

# Create your models here.
class Member (models.Model):
    userId = models.CharField(max_length=50 , verbose_name="아이디", primary_key=True)
    passwd = models.CharField(max_length=50, verbose_name="비밀번호", null=False)
    name = models.CharField(max_length=50, verbose_name="이름", null=False)
    gender = models.CharField(max_length=6, verbose_name="성별", null=False)
    address = models.CharField(max_length=500, verbose_name="주소", null=True)
    detailaddr = models.CharField(max_length=500, verbose_name="디테일주소", null=True)
    zonecode = models.CharField(max_length=5, verbose_name="우편번호", null=True)
    email = models.CharField(max_length=500, verbose_name="이메일", null=True)
    tel = models.CharField(max_length=30, verbose_name="전화번호", null=True, unique=True)
    signupdate = models.DateTimeField(auto_now_add=True, verbose_name="가입일", null=False, blank=True)
    modifydate = models.DateTimeField(auto_now_add=True, verbose_name="최근 수정일", null=False, blank=True)
    status = models.CharField(max_length=500, verbose_name="가입상태", null=False)
    age = models.CharField(max_length=50, verbose_name="나이", null=False)

class DeleteMember (models.Model):
    userId = models.CharField(max_length=50 , verbose_name="아이디")
    name = models.CharField(max_length=50, verbose_name="이름", null=False)
    gender = models.CharField(max_length=6, verbose_name="성별", null=False)
    address = models.CharField(max_length=500, verbose_name="주소", null=True)
    detailaddr = models.CharField(max_length=500, verbose_name="디테일주소", null=True)
    zonecode = models.CharField(max_length=5, verbose_name="우편번호", null=True)
    email = models.CharField(max_length=500, verbose_name="이메일", null=True)
    tel = models.CharField(max_length=30, verbose_name="전화번호", null=True)
    signupdate = models.DateTimeField(verbose_name="가입일")