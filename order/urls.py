from django.urls.conf import path
from order import views

app_name = "order"

urlpatterns = [
    path("order", views.OrderView.as_view(), name="order"),
    path("orderdone", views.OrderDoneView.as_view(), name="orderdone"),
    ]