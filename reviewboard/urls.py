from django.urls.conf import path
from reviewboard import views

app_name = "reviewboard"

urlpatterns = [
    path("reviewWrite", views.ReviewWriteView.as_view(), name="reviewWrite"),
    path("reviewModify", views.ReviewModifyView.as_view(), name="reviewModify"),
    path("reviewDelete", views.ReviewDeleteView.as_view(), name="reviewDelete"),
    path("myReviewList", views.MyReviewList.as_view(), name="myReviewList"),
    ]