from django.urls import path
from survey import views

app_name = "survey"
urlpatterns = [
    path("surveylist",views.SurveyView.as_view(),name="surveylist"),
]