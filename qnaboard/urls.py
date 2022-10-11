from django.urls.conf import path
from qnaboard import views

app_name = "qnaboard"

urlpatterns = [
    path( "qna", views.ListView.as_view(), name="qna" ),
    path( "writearticle", views.WriteView.as_view(), name="writearticle" ),
    path( "detailarticle", views.DetailView.as_view(), name="detailarticle" ),
    path( "deletearticle", views.DeleteView.as_view(), name="deletearticle" ),
    path( "modifyarticle", views.ModifyView.as_view(), name="modifyarticle" ),
    path( "myQnaList", views.MyQnaList.as_view(), name="myQnaList" ),
    ]
