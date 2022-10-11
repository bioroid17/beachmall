from django.contrib import admin
from qnaboard.models import Qnaboard

# Register your models here.
class QnaboardAdmin( admin.ModelAdmin ) :
    list_display = ( "qnaNum", "userId", "qnaTitle", "qnaContent",
                     "reply_title","reply_content" )
admin.site.register( Qnaboard, QnaboardAdmin )