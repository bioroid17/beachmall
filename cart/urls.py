from django.urls.conf import path
from cart import views

app_name = "cart"

urlpatterns = [
    path("cart", views.CartView.as_view(), name="cart"),
    path("cartins", views.CartInsView.as_view(), name="cartins"),
    path("cartdel", views.CartDelView.as_view(), name="cartdel"),
    path("cartmod", views.CartModView.as_view(), name="cartmod"),
]