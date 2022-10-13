from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from wishlist.models import Wishlist
from member.models import Member
from product.models import Product
import logging
# member, product, wishlist .. 등 사용할 것들을 추가적으로  import 하였다 

# logger 객체를 발행하도록 생성한 것임, (__name__) : 실행할 모듈명,사용자가 지정하는 로거의 이름
logger = logging.getLogger(__name__)

# Create your views here.

class WishView(View):
    def get(self, request):
        template = loader.get_template("wish.html") # wish.html에 출력한다
        memid = request.session.get("memid") # 세션(쿠키)의 memid 를 가져온다
        if not memid:   # 찜 목록 비로그인 접근 제한
            context= {
                "message" : "로그인 후 이용하실 수 있습니다."  # 비로그인 시 사용하는 메세지 
                }
        else: # 로그인 상태일 떄
            # objects.raw() 쿼리 실행문, Product_Product : p, Wishlist_Wishlist : w, on : 뒤에 나온 조건이 있을때 , order by : 해라 , 상품번호를 순서대로 나열
            wishlist = Wishlist.objects.raw(""" 
            select w.wishNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodNum
            from Product_Product p inner join Wishlist_Wishlist w
            on p.prodNum=w.prodNum and w.userId=%s
            order by wishNum desc
            """, (memid,)) # userId=%s : memid를 문자열로 포맷팅한다
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
                logger.info("id:"+memid+",,,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        return HttpResponse(template.render(context, request))
    def post(self, request):
        pass
    

class WishDelView(View):
    def get(self, request):
        wishNum = request.GET["wishNum"]
        if wishNum != "0":
            wish = Wishlist.objects.get(wishNum=wishNum)
            logger.info("id:"+wish.userId.userId+",wishNum:"+str(wishNum)+",prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
            wish.delete()
        else:
            userId = request.session.get("memid")
            wishlist = Wishlist.objects.filter(userId__exact=userId)
            for wish in wishlist:
                logger.info("id:"+userId+",wishNum:0,prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
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
            logger.info("id:"+userId+",,prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
            wish.save()
        return redirect("wishlist:wish")
    def post(self, request):
        pass