from django.urls.conf import path
from wishlist import views

app_name = "wishlist"

urlpatterns = [
    path("wish", views.WishView.as_view(), name="wish"),
    path("wishdel", views.WishDelView.as_view(), name="wishdel"),
    path("wishins", views.WishInsView.as_view(), name="wishins"),
]