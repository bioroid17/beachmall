from django.urls.conf import path
from product import views

app_name = "product"

urlpatterns = [
    path("productDetail", views.ProductDetailView.as_view(), name="productDetail"),
    path("productCategory", views.ProductCategoryView.as_view(), name="productCategory"),
    path("productList", views.ProductListView.as_view(), name="productList"),
    path("waterRocket", views.WaterRocketView.as_view(), name="waterrocket"),
    ]