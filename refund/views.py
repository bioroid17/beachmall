from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from refund.models import Refund
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from datetime import datetime


from member.models import Member
from order.models import OrderDetail
from product.models import Product

PAGE_SIZE = 5
PAGE_BLOCK = 3

# Create your views here.
class RefundListView(View):
    def get(self,request):
        template=loader.get_template("refundlist.html")
        userId = request.session.get("memid")
        refundscount=Refund.objects.filter(userId=userId).count()
        
        pagenum = request.GET.get( "pagenum" )
        if not pagenum :
            pagenum = "1"
        pagenum = int( pagenum )
        
        start = ( pagenum - 1 ) * int(PAGE_SIZE)          # ( 5 - 1 ) * 10 + 1     41
        end = start + int(PAGE_SIZE)                      # 41 + 10 - 1            50
        if end > refundscount :
            end = refundscount
        refunds= Refund.objects.filter(userId=userId).order_by("-refundProdNum")[start:end]
        number = refundscount - ( pagenum - 1 ) * int(PAGE_SIZE )
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1       # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0:
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = refundscount // int(PAGE_SIZE)
        if refundscount % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount
        pages = range( startpage, endpage+1 )
        
        context={
            "refunds":refunds,
            "refundscount":refundscount,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            }
        return HttpResponse(template.render(context,request))
    def post(self,request):
        pass

class RefundRegisterView(View):
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( RefundRegisterView ,self ).dispatch( request, *args, **kwargs)
    def get(self,request):
        template=loader.get_template("refund.html")
        orderDetailNum = request.GET.get("orderDetailNum")
        print(orderDetailNum)
        orderDetail = OrderDetail.objects.get(orderDetailNum=orderDetailNum)
        memid = request.session.get("memid")
        context={
            "memid":memid,
            "orderDetail":orderDetail
            }
        return HttpResponse(template.render(context,request))
    
    def post(self,request):
        orderDetailNum = request.POST["orderDetailNum"]
        orderDetail = OrderDetail.objects.get(orderDetailNum=orderDetailNum)
        refund_exchangecheck = request.POST["refund_exchangecheck"]
        dto = Refund(
            orderDetailNum = orderDetail,
            userId= request.POST["userId"], 
            reason = request.POST["reason"],
            refund_exchangecheck = refund_exchangecheck,
            refundPhoto = request.FILES.get("photo")
            )
        if refund_exchangecheck == "3":
            product = Product.objects.get(prodNum=orderDetail.prodNum)
            product.prodStock = product.prodStock - 1
            product.save()
        dto.save()
        orderDetail.is_refunded = True
        orderDetail.save()
        return redirect( "refund:myrefundlist" )