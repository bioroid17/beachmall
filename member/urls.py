from django.urls.conf import path
from member import views

app_name = "member"

urlpatterns = [
    path("login",views.LoginView.as_view(),name="login"),
    path('memberjoin', views.JoinView.as_view() ,name="memberjoin"),
    path("idconfirm", views.IdConfirmView.as_view(), name="idconfirm"), 
    path("telconfirm", views.TelConfirmView.as_view(), name="telconfirm"),
    path("logout", views.LogoutView.as_view(), name ="logout"),
    path("delete", views.DeleteView.as_view(), name="delete"), 
    path("modify", views.ModifyView.as_view(), name="modify"),
    path("modifypro", views.ModifyProView.as_view(), name="modifypro"),
    path("index",views.IndexView.as_view(), name="index"),
    path("myorderlist",views.MyOrderListView.as_view(), name="myorderlist"),
    path("myorderdetail",views.MyOrderDetailView.as_view(), name="myorderdetail"),
    path("mybeach",views.MyBeachView.as_view(), name="mybeach"),
    path("papup",views.PapUpView.as_view(), name="papup"),
]
