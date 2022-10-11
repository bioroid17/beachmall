from noticeboard import views
from django.urls.conf import path

app_name = "noticeboard"

urlpatterns = [
    path("noticelist", views.NoticeView.as_view(), name="noticelist"),
    path("noticedetail", views.NoticeDetailView.as_view(), name="noticedetail"),
    ]