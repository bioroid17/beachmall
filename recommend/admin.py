from django.contrib import admin
from recommend.models import Recommend

# Register your models here.
class RecommendAdmin(admin.ModelAdmin):
    list_display = ("recommendNum","prodNum","status")

admin.site.register(Recommend, RecommendAdmin)