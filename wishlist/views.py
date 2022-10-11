from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from wishlist.models import Wishlist
from member.models import Member
from product.models import Product
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class WishView(View):
    def get(self, request):
        template = loader.get_template("wish.html")
        memid = request.session.get("memid")
        if not memid:   # 찜 목록 비로그인 접근 제한
            context= {
                "message" : "로그인 후 이용하실 수 있습니다."
                }
        else:
            wishlist = Wishlist.objects.raw("""
            select w.wishNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodNum
            from Product_Product p inner join Wishlist_Wishlist w
            on p.prodNum=w.prodNum and w.userId=%s
            order by wishNum desc
            """, (memid,))
            if wishlist:
                context = {
                    "wishlist" : wishlist,
                    "memid" : memid,
                    }
            else:
                context = {
                    "message" : "찜 목록이 비었습니다.",
                    "memid" : memid,
                    }
        print(request.META.HTTP_REFERER, request.path)
        # logger.info()
        return HttpResponse(template.render(context, request))
    def post(self, request):
        pass
    

class WishDelView(View):
    def get(self, request):
        wishNum = request.GET["wishNum"]
        if wishNum != "0":
            wish = Wishlist.objects.get(wishNum=wishNum)
            wish.delete()
        else:
            userId = request.session.get("memid")
            wishlist = Wishlist.objects.filter(userId__exact=userId)
            for wish in wishlist:
                wish.delete()
        return redirect("wishlist:wish")
    def post(self, request):
        pass
    
class WishInsView(View):
    def get(self, request):
        userId = request.GET["userId"]
        prodNum = request.GET["prodNum"]
        count = Wishlist.objects.filter(prodNum=prodNum).filter(userId=userId).count()
        if userId and count == 0:
            wish = Wishlist(
                userId = Member.objects.get(userId=userId),
                prodNum = Product.objects.get(prodNum=prodNum),
                )
            wish.save()
        print(request.path)
        return redirect("wishlist:wish")
    def post(self, request):
        pass