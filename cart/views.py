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
        else:
            carts = Cart.objects.raw("""
            select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, c.buyCount, p.prodStock, p.prodPrice*c.buyCount prodTotal
            from Product_Product p inner join Cart_Cart c
            on p.prodNum=c.prodNum and c.userId=%s
            order by cartNum desc
            """, (memid,))
            totalPrice = 0
            if carts:
                for cart in carts:
                    totalPrice += cart.prodTotal
                context = {
                    "carts" : carts,
                    "memid" : memid,
                    "totalPrice" : totalPrice
                    }
            else:
                context = {
                    "message" : "장바구니가 비었습니다.",
                    "memid" : memid,
                    "totalPrice" : totalPrice
                    }
            logger.info("id : " + memid + "\tcart.html")
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
        count = Cart.objects.filter(prodNum=prodNum).filter(userId=userId).count()
        if userId and count == 0:
            cart = Cart(
                userId = Member.objects.get(userId=userId),
                prodNum = Product.objects.get(prodNum=prodNum),
                buyCount = request.GET["buyCount"]
                )
            cart.save()
        return redirect("cart:cart")
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
        if cartNum != "0":
            cart = Cart.objects.get(cartNum=cartNum)
            cart.delete()
        else:
            userId = request.session.get("memid")
            carts = Cart.objects.filter(userId__exact=userId)
            for cart in carts:
                cart.delete()
        return redirect("cart:cart")
    def post(self, request):
        pass

class CartModView(View):
    def get(self, request):
        cartNum = request.GET["cartNum"]
        cart = Cart.objects.get(cartNum=cartNum)
        cart.buyCount = request.GET["buyCount"]
        cart.save()
        return redirect("cart:cart")
    def post(self, request):
        pass