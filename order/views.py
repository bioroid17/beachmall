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
import logging

logger = logging.getLogger(__name__)

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
        # 로그인이 안되어 있을 당시
        if not memid:
            context= {
                "message" : "로그인 후 이용하실 수 있습니다.",
                }
        else:
        # 로그인시
            member = Member.objects.get(userId=memid)
        # 카트와 상품을 iNNERjOIN해준다 카트의 상품번호와 상품테이블의 상품번호 같은것을 갖고온다 상품테이블의 가격과 카트의 갯수를 곱해준다.
            carts = Cart.objects.raw("""
            select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
            from Product_Product p inner join Cart_Cart c
            on p.prodNum=c.prodNum and c.userId=%s
            order by cartNum desc
            """, (memid,))
            totalPrice = 0
            # carts에서 하나씩 빼서 더해준다. 총가격을 만들어준다.
            for cart in carts:
                totalPrice += cart.prodTotal
            context = {
                "carts" : carts,
                "memid" : memid,
                "member" : member,
                "totalPrice" : totalPrice
                }
            logger.info("id:"+memid+",,,,,,,,from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        return HttpResponse(template.render(context, request))
    """
    입력한 수취인의 정보를 post 방식으로 넘길 때 실행한다.
    orderinfo.html을 렌더링한다.
    이 페이지는 주문자, 수취인, 상품 정보를 최종적으로 확인하고 구매 확정 여부를 묻는다.
    """
    def post(self, request):
        template = loader.get_template("orderinfo.html")
        userId = request.POST["userId"]
        # 카트와 상품을 iNNERjOIN해준다 카트의 상품번호와 상품테이블의 상품번호 같은것을 갖고온다 상품테이블의 가격과 카트의 갯수를 곱해준다.
        carts = Cart.objects.raw("""
        select c.cartNum, p.prodName, p.prodThumbnail, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
        from Product_Product p inner join Cart_Cart c
        on p.prodNum=c.prodNum and c.userId=%s
        order by cartNum desc
        """, (userId,))
        
        #cart.html에서 입력한갑을 orderINFO에 갖고온 것
        getterName = request.POST["getterName"]
        getterTel = request.POST["getterTel"]
        getterZonecode = request.POST["getterZonecode"]
        getterAddress = request.POST["getterAddress"]
        getterDetailAddr = request.POST["getterDetailAddr"]
        totalPrice = request.POST["totalPrice"]
        
        context = {
            "name" : request.POST["name"],
            "tel" : request.POST["tel"],
            "userId" : userId,
            "getterName" : getterName,
            "getterTel" : getterTel,
            "getterZonecode" : getterZonecode,
            "getterAddress" : getterAddress,
            "getterDetailAddr" : getterDetailAddr,
            "requirement" : request.POST["requirement"],
            "orderMsg" : request.POST["orderMsg"],
            "carts" : carts,
            "totalPrice" : totalPrice,
            }
        logger.info("id:"+userId+",,getterName:"+getterName+",getterTel:"+getterTel+",getterZonecode:"+getterZonecode+",getterAddress:"+getterAddress+
                    ",getterDetailAddr:"+getterDetailAddr+",totalPrice:"+totalPrice+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        
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
        #CART와 상품의 비교를위해 ㅇINNERJOIN해준다
        carts = Cart.objects.raw("""
        select c.cartNum, p.prodName, p.prodNum, p.prodPrice, p.prodStock, c.buyCount, p.prodPrice*c.buyCount prodTotal
        from Product_Product p inner join Cart_Cart c
        on p.prodNum=c.prodNum and c.userId=%s
        order by cartNum desc
        """, (userId,))
        #카트와 상품재고 하나씩 비교해주기위해 
        for cart in carts:
            if cart.prodStock < cart.buyCount:
                context = {
                    "message" : "현재 장바구니의 상품 중 수량이 현재 재고를 넘는 것이 있어서 주문에 실패했습니다. 상품 수량을 다시 선택해주세요."
                    }
                return HttpResponse(template.render(context, request))
        
        #오더에서 넘어온 값들을 받느다.
        getterName = request.POST["getterName"]
        getterTel = request.POST["getterTel"]
        getterZonecode = request.POST["getterZonecode"]
        getterAddress = request.POST["getterAddress"]
        getterDetailAddr = request.POST["getterDetailAddr"]
        totalPrice = request.POST["totalPrice"]
        #오더 테이블에 저장해준다.
        order = Order(
            userId = userId,
            getterName = getterName,
            getterTel = getterTel,
            getterZonecode = getterZonecode,
            getterAddress = getterAddress,
            getterDetailAddr = getterDetailAddr,
            requirement = request.POST["requirement"],
            orderMsg = request.POST["orderMsg"],
            totalPrice = totalPrice,
            )
        order.save()
        #최신 ORDERNUM을 갖고온다.
        orderNum = Order.objects.order_by("-orderNum").first()
        #bulk_create 대량의 데이터를 INSERT해주기 위해 사용한다. 카트안에 있는 상품별로 객체를 설정해서 상품별 
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
        
        logger.info("id:"+userId+",orderNum:"+str(orderNum)+",getterName:"+getterName+",getterTel:"+getterTel+",getterZonecode:"+str(getterZonecode)+",getterAddress:"+getterAddress+
                    ",getterDetailAddr:"+getterDetailAddr+",totalPrice:"+totalPrice+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
        
        return HttpResponse(template.render(context, request))
    
    
    
    
    
    
    
    
    
    
    
    
    
    