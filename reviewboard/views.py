from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from reviewboard.models import Reviewboard
from product.models import Product
from django.http.response import HttpResponse
from django.template import loader
from django.utils.dateformat import DateFormat
from datetime import datetime
import logging

PAGE_SIZE = 15
PAGE_BLOCK = 5

logger = logging.getLogger( __name__ )
# Create your views here.
class ReviewWriteView(View):
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( ReviewWriteView ,self ).dispatch( request, *args, **kwargs )
    def get(self, request ) :
        pass
    def post(self, request ) :
        prodNum = request.POST["prodNum"]
        review = Reviewboard(
            userId = request.POST["userId"],
            prodNum = Product.objects.get(prodNum=prodNum),
            reviewTitle = request.POST["reviewTitle"],
            reviewContent = request.POST["reviewContent"],
            reviewIp = request.META.get( "REMOTE_ADDR" ),
            reviewPhoto = request.FILES.get("reviewPhoto"),
            )
        review.save()
        return redirect( "member:myorderlist" )  

class ReviewModifyView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( ReviewModifyView,self ).dispatch( request, *args, **kwargs)
    def get(self, request ) :
        pass
    def post(self, request) : # post만 구현하면 된다
        reviewNum = request.POST["reviewNum"]
        review = Reviewboard.objects.get(reviewNum=reviewNum)
        review.reviewTitle = request.POST["reviewTitle"]
        review.reviewContent = request.POST["reviewContent"]
        review.reviewPhoto = request.FILES.get("reviewPhoto")
        review.reviewIp = request.META.get("REMOTE_ADDR")
        review.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
    
class ReviewDeleteView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( ReviewDeleteView,self ).dispatch( request, *args, **kwargs)
    def get(self, request ) :
        pass
    def post(self, request ) :
        reviewNum = request.POST["reviewNum"]
        review = Reviewboard.objects.get(reviewNum=reviewNum)
        review.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
    
class MyReviewList (View):
    def get(self, request):
        
        userId = request.session.get("memid")
        count = Reviewboard.objects.filter(userId=userId).count()
        reviewboards = Reviewboard.objects.filter(userId=userId)
        
        pagenum = request.GET.get("pagenum")
        if not pagenum :
            pagenum = "1"
        pagenum = int(pagenum)
        
        start = (pagenum - 1) * int(PAGE_SIZE)      # (5 - 1) * 10    = 40    슬라이싱을 위해 0~10까지 잡기
        end = start + int(PAGE_SIZE)                # 40 + 10         = 50
        if end > count :
            end = count
        reviews = Reviewboard.objects.order_by("-reviewNum")[start:end]
        number = count - (pagenum - 1) * int(PAGE_SIZE)
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1    # 9 // 10 * 10 + 1     = 1
        if pagenum % int(PAGE_BLOCK) == 0:
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                       # 1 + 10 - 1           = 10
        pagecount = count // int(PAGE_SIZE)
        if count % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount:
            endpage = pagecount
        pages = range(startpage, endpage + 1)
        context={
                "userId":userId,
                "count" : count,
                "reviewboards":reviewboards,
                "pagenum" : pagenum,
                "number" : number,
            }
        
        template = loader.get_template("myReviewList.html")
        return HttpResponse( template.render( context, request ) )    