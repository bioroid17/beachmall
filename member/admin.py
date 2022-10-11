from django.contrib import admin
from member.models import Member, DeleteMember

# Register your models here.
class MemberAdmin (admin.ModelAdmin):
                #컬럼이름을 줘야한다.
    list_display=("userId", "passwd", "name", "gender", "address", "detailaddr",
                  "zonecode", "email", "tel", "signupdate", "modifydate", "status")
    
admin.site.register(Member, MemberAdmin)

class DeleteMemberAdmin (admin.ModelAdmin):
                #컬럼이름을 줘야한다.
    list_display=("userId", "name", "gender", "address", "detailaddr",
                  "zonecode", "email", "tel", "signupdate")
    
admin.site.register(DeleteMember, DeleteMemberAdmin)