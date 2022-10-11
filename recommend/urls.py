from django.urls.conf import path
from recommend import views
urlpatterns = [
    path('bestprod', views.BestprodView.as_view(),name="bestprod"),
    
]