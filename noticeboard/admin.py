from django.contrib import admin
from noticeboard.models import NoticeBoard

# Register your models here.
class NoticeBoardAdmin (admin.ModelAdmin):
    list_display=("noticeNum", "admin", "noticeTitle" , "noticeContent", "noticeDate" )
    
admin.site.register(NoticeBoard,NoticeBoardAdmin)