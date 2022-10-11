from django.urls.conf import path
from refund import views
app_name="refund"
urlpatterns = [
    path('myrefundlist', views.RefundListView.as_view(),name="myrefundlist"),
    path('refundregister', views.RefundRegisterView.as_view(),name="refundregister"),   
]

