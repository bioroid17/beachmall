from django.db import models

# Create your models here.
class Survey(models.Model):
    #관리자가 관리하는 디비
    #   survey 아이디          자동인식증가
    survey_idx  = models.AutoField(primary_key=True)
    #질문
    question1 = models.TextField(null=False)
    #답변이 들어갈 컬럼
    ans1 = models.TextField(null=False)
    ans2 = models.TextField(null=False)
    
    question2 = models.TextField(null=False)
    ans3 = models.TextField(null=False)
    ans4 = models.TextField(null=False)
    
    question3 = models.TextField(null=False)
    ans5 = models.TextField(null=False)
    ans6 = models.TextField(null=False)
    
    question4 = models.TextField(null=False)
    ans7 = models.TextField(null=False)
    ans8 = models.TextField(null=False)
    
    question5 = models.TextField(null=False)
    ans9 = models.TextField(null=False)
    ans10 = models.TextField(null=False)
   
    status = models.CharField(max_length=1 , default="y")
    
#응답 디비
class Answer( models.Model):
     answer_idx  = models.AutoField(primary_key=True)
     #survey한 아이디 저장할곳 조인 할곳 위에 테이블과
     survey_idx  = models.IntegerField()
     #응답한것 답변 저장할 곳
     userId = models.ForeignKey("member.Member", on_delete=models.CASCADE, db_column="userId") 

     num = models.IntegerField()
     num1 = models.IntegerField()
     num2 = models.IntegerField()
     num3 = models.IntegerField()
     num4 = models.IntegerField()