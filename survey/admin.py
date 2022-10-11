from django.contrib import admin
from survey.models import Survey

# Register your models here.
#admin은 어플생성 하면 생기고 거기에서 admin디비에서 surveydb연결 등록해준다.
class SurveyAdmin (admin.ModelAdmin):
                #컬럼이름을 줘야한다.
    list_display=("survey_idx","question1","ans1","ans2","question2","ans3","ans4","question3","ans5","ans6","question4","ans7","ans8","question4","ans9","ans10","status")
                    #Survey어플과 SurveyAdmin(현재 admin) 연결
admin.site.register(Survey,SurveyAdmin)