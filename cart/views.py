from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from cart.models import Cart
from product.models import Product
from member.models import Member
import logging

# Create your views here.
logger = logging.getLogger(__name__)
"""
장바구니 목록 페이지
"""
class CartView(View):
    def get(self, request):
        template = loader.get_template("cart.html")
        memid = request.session.get("memid")
        if not memid:   # 장바구니 비로그인 접근 제한
            context= {
                "message" : "로그인 후 이용하실 수 있습니다.",
                }
        else:       # Cart 는 model이름
            carts = Cart.objects.raw("""
            select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, c.buyCount, p.prodStock, p.prodPrice*c.buyCount prodTotal
            from Product_Product p inner join Cart_Cart c
            on p.prodNum=c.prodNum and c.userId=%s
            order by cartNum desc
            """, (memid,))
            totalPrice = 0      # 총 금액 가격을 0으로 지정해 놓음
            if carts:   # 키트가 있을 떄
                for cart in carts:      # carts 를 cart 로 반복문 돌려서
                    totalPrice += cart.prodTotal        # 상품 금액을 모두 더한다
                context = {     # 카트목록과 아이디 가격을 웹페이지로 넘긴다 
                    "carts" : carts,
                    "memid" : memid,
                    "totalPrice" : totalPrice
                    }
            else:   # 카트가 없을때 
                context = {
                    "message" : "장바구니가 비었습니다.",
                    "memid" : memid,
                    "totalPrice" : totalPrice
                    }
            logger.info("id:"+memid+",,,,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        return HttpResponse(template.render(context, request))
    def post(self, request):
        pass
    
"""
장바구니에 상품을 넣을 때 실행된다.
"""
class CartInsView(View):
    def get(self, request):
        userId = request.GET["userId"]
        prodNum = request.GET["prodNum"]
        buyCount = request.GET["buyCount"]
        count = Cart.objects.filter(prodNum=prodNum).filter(userId=userId).count()      # 상품번호 같고 아이디가 같은것을 센다
        if userId and count == 0:       # userId가 있고 count가 0일 떄
            cart = Cart(                # userId 와 prodNum , buyCount 담는다 ,  
                userId = Member.objects.get(userId=userId),
                prodNum = Product.objects.get(prodNum=prodNum),
                buyCount = buyCount
                )                                                                                                                                                                   
            logger.info("id:"+userId+",,prodNum:"+str(cart.prodNum.prodNum)+",buyCount:"+buyCount+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())     # log 저장
            cart.save()         # 담긴 정보를 저장함
        return redirect("cart:cart")    # cart 페이지로 쏜다
    def post(self, request):
        pass

"""
cart 페이지에서 장바구니 항목 삭제 시 실행
장바구니 항목을 개별 삭제 시와 '장바구니 비우기' 버튼을 통한 일괄 삭제
장바구니 비우기 버튼은 cartNum이 넘어오지 않는다.
"""
class CartDelView(View):
    def get(self, request):
        cartNum = request.GET.get("cartNum")
        userId = request.session.get("memid")
        if cartNum != "0":          # 카트번호가 0이 아닐떄 삭제
            cart = Cart.objects.get(cartNum=cartNum)
            logger.info("id:"+cart.userId.userId+",cartNum:"+cartNum+",prodNum:"+str(cart.prodNum.prodNum)+",,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
            cart.delete()
        else:   # 카트번호가 0일 때 모두 삭제
            carts = Cart.objects.filter(userId__exact=userId)
            for cart in carts:
                logger.info("id:"+userId+",cartNum:0,prodNum:"+str(cart.prodNum.prodNum)+",,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
                cart.delete()
        return redirect("cart:cart")
    def post(self, request):
        pass

class CartModView(View):
    def get(self, request):
        cartNum = request.GET["cartNum"]
        buyCount = request.GET["buyCount"]
        cart = Cart.objects.get(cartNum=cartNum)    # 프라이머리키를 가져옴
        cart.buyCount = buyCount    # cart.buyCount에 웹사이트에서 받아온 buyCount를 담음
        logger.info("id:"+cart.userId.userId+",cartNum:"+cartNum+",prodNum:"+str(cart.prodNum.prodNum)+",buyCount:"+buyCount+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        cart.save()     # DB에 저장한다
        return redirect("cart:cart")
    def post(self, request):
        pass