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
            if wishlist: # 찜 목록이 있다면 아이디와 찜목록을 가져온다
                context = {
                    "wishlist" : wishlist,
                    "memid" : memid,
                    }
            else: # 찜 목록이 비었을 떄 , 출력할 메시지를 만들고 , memid를 가져와 지정한다
                context = {
                    "message" : "찜 목록이 비었습니다.",
                    "memid" : memid,
                    }                                   # 지금 있는 페이지(http_referer)와 어떤 페이지로 넘어가는지(get_full_path)를 나타냄
                logger.info("id:"+memid+",,,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path()) # id ,,,from:wishNum,prodNum등을 생략한다는 의미로 사용
        return HttpResponse(template.render(context, request))
    def post(self, request):
        pass
    
# 찜 삭제
class WishDelView(View):
    def get(self, request):
        wishNum = request.GET["wishNum"] # 찜 번호를 가져옴
        if wishNum != "0":  # 찜번호가 0이 아닐때
            wish = Wishlist.objects.get(wishNum=wishNum) # 찜 목록에 찜 번호가 같은 것을 wish에 넣음
            # id, wishNum, prodNum, from: 현제 페이지와 넘어가는 페이지를 기록한다
            logger.info("id:"+wish.userId.userId+",wishNum:"+str(wishNum)+",prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
            wish.delete() # 찜 목록에 상품을 삭제 한다
        else: # 찜 번호가 0 일 때
            userId = request.session.get("memid") # memid 를 가져온다 
            wishlist = Wishlist.objects.filter(userId__exact=userId)    # 찜목록
            for wish in wishlist:   # 찜 목록 리스트를 wish로 반복문 돌림, 아래 로그를 남기고 , 찜 목록이 있다면 삭제
                logger.info("id:"+userId+",wishNum:0,prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
                wish.delete()
        return redirect("wishlist:wish")    # 찜목록 페이지로 넘김
    def post(self, request):
        pass
# 찜 넣기
class WishInsView(View):
    def get(self, request):
        userId = request.GET["userId"]
        prodNum = request.GET["prodNum"]
        count = Wishlist.objects.filter(prodNum=prodNum).filter(userId=userId).count()  # 같은 상품번호 같은 아이디를 카운트
        if userId and count == 0:   # 유저 아이디가 있을떄 그리고 카운트가 0 일 때 ,같은 상품이 안들어가게함
            wish = Wishlist(        # 아이디와 상품을 wish에 넣는다
                userId = Member.objects.get(userId=userId),
                prodNum = Product.objects.get(prodNum=prodNum),
                )               # 로그를 쌓는다
            logger.info("id:"+userId+",,prodNum:"+str(wish.prodNum.prodNum)+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
            wish.save()
        return redirect("wishlist:wish")    # wish 페이지로 던진다
    def post(self, request):
        pass