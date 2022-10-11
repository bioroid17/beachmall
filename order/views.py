from django.shortcuts import render
from django.views.generic.base import View
from member.models import Member
from django.template import loader
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from order.models import Order, OrderDetail
from product.models import Product

# Create your views here.
class OrderView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderView, self).dispatch(request , *args, **kwargs)
    """
    장바구니 페이지에서 구매하기 버튼을 누르면 실행.
    넘길 데이터가 없으므로 get 방식으로 실행한다.
    order.html을 렌더링한다. 이 페이지에서는 수취인의 정보를 입력한다.
    """
    def get(self, request):
        template = loader.get_template("order.html")
        memid = request.session.get("memid")
        
        if not memid:
            context= {
                "message" : "로그인 후 이용하실 수 있습니다.",
                }
        else:
            member = Member.objects.get(userId=memid)
            
            carts = Cart.objects.raw("""
            select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
            from Product_Product p inner join Cart_Cart c
            on p.prodNum=c.prodNum and c.userId=%s
            order by cartNum desc
            """, (memid,))
            totalPrice = 0
            for cart in carts:
                totalPrice += cart.prodTotal
            context = {
                "carts" : carts,
                "memid" : memid,
                "member" : member,
                "totalPrice" : totalPrice
                }
        return HttpResponse(template.render(context, request))
    """
    입력한 수취인의 정보를 post 방식으로 넘길 때 실행한다.
    orderinfo.html을 렌더링한다.
    이 페이지는 주문자, 수취인, 상품 정보를 최종적으로 확인하고 구매 확정 여부를 묻는다.
    """
    def post(self, request):
        template = loader.get_template("orderinfo.html")
        userId = request.session.get("memid")
        carts = Cart.objects.raw("""
        select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
        from Product_Product p inner join Cart_Cart c
        on p.prodNum=c.prodNum and c.userId=%s
        order by cartNum desc
        """, (userId,))
        context = {
            "name" : request.POST["name"],
            "tel" : request.POST["tel"],
            "userId" : userId,
            "getterName" : request.POST["getterName"],
            "getterTel" : request.POST["getterTel"],
            "getterZonecode" : request.POST["getterZonecode"],
            "getterAddress" : request.POST["getterAddress"],
            "getterDetailAddr" : request.POST["getterDetailAddr"],
            "requirement" : request.POST["requirement"],
            "orderMsg" : request.POST["orderMsg"],
            "carts" : carts,
            "totalPrice" : request.POST["totalPrice"],
            }
        
        return HttpResponse(template.render(context, request))

class OrderDoneView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderDoneView, self).dispatch(request , *args, **kwargs)
    def get(self, request):
        pass
    """
    orderdone.html을 렌더링한다.
    이 페이지에서는 회원이 구매를 확정지었으므로
    orderinfo.html에서 hidden으로 넘어온 데이터를 받아서 DB에 저장한다.
    """
    def post(self, request):
        template = loader.get_template("orderdone.html")
        
        context = {}
        userId = request.POST["userId"]
        carts = Cart.objects.raw("""
        select c.cartNum, p.prodName, p.prodNum, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
        from Product_Product p inner join Cart_Cart c
        on p.prodNum=c.prodNum and c.userId=%s
        order by cartNum desc
        """, (userId,))
        
        for cart in carts:
            if cart.prodStock < cart.buyCount:
                context = {
                    "message" : "현재 장바구니의 상품 중 수량이 현재 재고를 넘는 것이 있어서 주문에 실패했습니다. 상품 수량을 다시 선택해주세요."
                    }
                return HttpResponse(template.render(context, request))
        
        order = Order(
            userId = userId,
            getterName = request.POST["getterName"],
            getterTel = request.POST["getterTel"],
            getterZonecode = request.POST["getterZonecode"],
            getterAddress = request.POST["getterAddress"],
            getterDetailAddr = request.POST["getterDetailAddr"],
            requirement = request.POST["requirement"],
            orderMsg = request.POST["orderMsg"],
            totalPrice = request.POST["totalPrice"],
            )
        order.save()
        
        orderNum = Order.objects.order_by("-orderNum").first()
        
        OrderDetail.objects.bulk_create(
            [OrderDetail(
                orderNum=orderNum,
                prodNum = cart.prodNum.prodNum,
                prodName = cart.prodName,
                prodThumbnail = cart.prodNum.prodThumbnail.url,
                prodPrice = cart.prodPrice,
                buyCount = cart.buyCount,
                prodTotal = cart.prodTotal,
                ) for cart in carts]
            )
        
        for cart in carts:
            product = Product.objects.get(prodNum=cart.prodNum.prodNum)
            product.prodStock -= cart.buyCount
            product.save()
            cart.delete()
        
        return HttpResponse(template.render(context, request))
    
    
    
    
    
    
    
    
    
    
    
    
    
    