from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from qnaboard.models import Qnaboard
import logging
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
logger = logging.getLogger( __name__ )

PAGE_SIZE = 5
PAGE_BLOCK = 3

# QnA 리스트 페이지
class ListView( View ) :
    def get(self, request ) :
        template = loader.get_template( "qna.html" )
        count = Qnaboard.objects.all().count()
        
        pagenum = request.GET.get( "pagenum" )
        if not pagenum :
            pagenum = "1"
        pagenum = int( pagenum )
        
        start = ( pagenum - 1 ) * int(PAGE_SIZE)          # ( 5 - 1 ) * 10 + 1     41
        end = start + int(PAGE_SIZE)                      # 41 + 10 - 1            50
        if end > count :
            end = count
        dtos = Qnaboard.objects.order_by( "-qnaNum" )[start:end] # jsp와 다르게 슬라이싱해서 씀
        number = count - ( pagenum - 1 ) * int(PAGE_SIZE )
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1       # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0:
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = count // int(PAGE_SIZE)
        if count % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount
        pages = range( startpage, endpage+1 )
        context = {
            "count" : count,
            "dtos" : dtos,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            }
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        pass
    
# 글쓰기 페이지    
class WriteView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( WriteView,self ).dispatch( request, *args, **kwargs)
    def get(self, request ) :
        userId = request.session.get("memid")
            
        template = loader.get_template( "writearticle.html" )
        context = {
            "userId":userId,
            }
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        
        dto = Qnaboard(
            userId = request.POST["userId"],
            qnaTitle = request.POST["qnaTitle"],
            qnaContent = request.POST["qnaContent"],
            qnaScore=0,                                     #글쓸때 조회수는 0
            qnaDate = DateFormat( datetime.now() ).format( "Ymd" ),
            qnaIp = request.META.get( "REMOTE_ADDR" )
            )
        dto.save()
        return redirect( "qnaboard:qna" ) #app name 설정 때문에 board:list 로 해야함

# QnA 글 상세정보
class DetailView( View ) :
    def get(self, request ) :
        qnaNum = request.GET["qnaNum"]
        pagenum = request.GET["pagenum"]
        number = request.GET["number"]
        memid = request.session.get("memid")
        dto = Qnaboard.objects.get( qnaNum = qnaNum )
        if dto.qnaIp != request.META.get( "REMOTE_ADDR" ) :
            dto.qnaScore += 1
            dto.save()
        context = {
            "memid":memid,
            "qnaNum" : qnaNum,
            "pagenum" : pagenum,
            "number" : number,
            "dto" : dto,
            }
        template = loader.get_template( "detailarticle.html" )
        return HttpResponse( template.render( context, request ) )
        
    def post(self, request ) :
        pass
    
# QnA 글 삭제    
class DeleteView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( DeleteView,self ).dispatch( request, *args, **kwargs)
    
    def get(self, request ) :
        pass
             
    def post(self, request ) :
        qnaNum = request.POST["qnaNum"]
        dto = Qnaboard.objects.get( qnaNum = qnaNum )
        
            # 비밀번호가 같다
        logger.info( str(qnaNum)+","+dto.userId )
        dto.delete()
        return redirect( "qnaboard:qna" )

# QnA 글 수정
class ModifyView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( ModifyView,self ).dispatch( request, *args, **kwargs)
    
    def get(self, request ) :
        qnaNum = request.GET["qnaNum"]
        pagenum = request.GET["pagenum"]
        dto = Qnaboard.objects.get( qnaNum = qnaNum )
        
        template = loader.get_template( "modifyarticle.html" )
        context = {
                "qnaNum" : qnaNum,
                "pagenum" : pagenum,
                "dto" : dto,
                }
        return HttpResponse( template.render( context, request ) )
    
    def post(self, request ) :
        qnaNum = request.POST["qnaNum"]
        dto = Qnaboard.objects.get( qnaNum = qnaNum ) 
        dto.qnaTitle = request.POST["qnaTitle"]
        dto.qnaContent = request.POST["qnaContent"]
        dto.save()
        return redirect( "qnaboard:qna" )
# 내 QnA 글 리스트       
class MyQnaList (View):
    def get(self, request):
        userId = request.session.get("memid")
        count = Qnaboard.objects.filter(userId=userId).count()
        
        pagenum = request.GET.get( "pagenum" )
        if not pagenum :
            pagenum = "1"
        pagenum = int( pagenum )
        
        start = ( pagenum - 1 ) * int(PAGE_SIZE)          # ( 5 - 1 ) * 10 + 1     41
        end = start + int(PAGE_SIZE)                      # 41 + 10 - 1            50
        if end > count :
            end = count
        qnaboards = Qnaboard.objects.filter(userId=userId).order_by( "qnaNum" )[start:end] # jsp와 다르게 슬라이싱해서 씀
        number = count - ( pagenum - 1 ) * int(PAGE_SIZE )
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1       # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0:
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = count // int(PAGE_SIZE)
        if count % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount
        pages = range( startpage, endpage+1 )
        context={
                "userId":userId,
                "count" : count,
                "qnaboards":qnaboards,
                "pagenum" : pagenum,
                "number" : number,
                "pages" : pages,
                "startpage" : startpage,
                "endpage" : endpage,
                "pageblock" : PAGE_BLOCK,
                "pagecount" : pagecount,
            }
        
        template = loader.get_template("myQnaList.html")
        return HttpResponse( template.render( context, request ) )
    
    
    
    
    
    
    
    