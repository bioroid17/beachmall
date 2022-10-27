from django.contrib import admin
from recommend.models import Recommend

# Register your models here.
class RecommendAdmin(admin.ModelAdmin):
    list_display = ("recommendNum", "userId", "prodList", "status")

admin.site.register(Recommend, RecommendAdmin)