from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from django.utils.dateformat import DateFormat
from member.models import Member, DeleteMember
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django import template
from recommend.models import Recommend
from survey.models import Answer
from order.models import Order, OrderDetail
from product.models import Product
from cart.models import Cart
from refund.models import Refund
from product.choice import BRAND_CHOICE
import logging, csv
from static.myfunction import realtimeSearch, recommendByCartWishOrder, gender_age_recommend
import json

PAGE_SIZE = 5
PAGE_BLOCK = 3

logger = logging.getLogger(__name__)

#메인
class IndexView(View):
    def get (self,request):
        userId = request.session.get("memid")
        
        #로그를 이용해서 최근본 상품을 사용한다.
        productlog = open("log/productlog.log", 'r', encoding="utf-8")
        lines = csv.reader(productlog)  #전체 productlog하는 것을 갖고오는 것
        
        recents = []
        mostViews = {}
        count = 0
        today = datetime.today()
        for line in reversed(list(lines)):
            # 최대 일주일 치 로그만 분석한다.
            if datetime.strptime(line[0][1:11], "%Y-%m-%d") < today - timedelta(days=7):
                break
            id = line[3].split(":")[1]
            if id != userId:
                continue
            if line[4] == "" or line[4] == None:
                continue
            prodNum = line[4].split(":")[1]
            if Product.objects.filter(prodNum=prodNum).count() == 0:
                continue
            if str(prodNum) in mostViews:
                mostViews[str(prodNum)] += 1
            else:
                mostViews[str(prodNum)] = 1
            if count >= 4:
                continue
            else:
                if prodNum not in recents:
                    recents.append(prodNum)
                    count += 1
        recentProducts = [Product.objects.get(prodNum=recent) for recent in recents]
        
        views_sorted = [(key, value) for key, value in mostViews.items()][0:5]
        views_sorted.sort(key=lambda x:x[1], reverse=True)
        
        frequentProducts = [Product.objects.get(prodNum=prodNum) for prodNum, searchCount in views_sorted]
        
        productlog.close()
        
        gender_age_recos = []
        if userId:
            try:
                recos = Recommend.objects.filter(userId=userId).filter(status="gender_age").order_by("-recommendNum").first().prodList
                recommends = json.loads(recos)
                gender_age_recos = [Product.objects.get(prodNum=prodNum) for prodNum in recommends]
            except (ObjectDoesNotExist, AttributeError):
                gender_age_recos = []
        #OrderDetail.prodNum과 Product.prodNum 같은것을 연결해준. hotdeal객체를 사용하여 많이 구매한 상품을 띄어준다
        hotdeals = OrderDetail.objects.raw("""
        select od.orderDetailNum, od.orderNum, od.prodName, od.prodPrice, od.prodThumbnail, p.prodNum, p.brand
        from order_OrderDetail od, product_product p where od.prodNum=p.prodNum
        group by od.prodNum
        order by sum(buyCount) DESC LIMIT 5
        """)
        
        rts = realtimeSearch()
        ordercounts = Order.objects.filter(userId=userId).count()
        cartwishorder_recos = []
        if ordercounts > 0:
            try:
                recos = Recommend.objects.filter(userId=userId).filter(status="cart_wish_order").order_by("-recommendNum").first().prodList
                recommends = json.loads(recos)
                cartwishorder_recos = [Product.objects.get(prodNum=prodNum) for prodNum in recommends]
            except (ObjectDoesNotExist, AttributeError):
                cartwishorder_recos = []
        context={
            "cartwishorder_recos":cartwishorder_recos,
            "userId":userId,
            "recentProducts":recentProducts,
            "brands":BRAND_CHOICE,
            "frequentProducts":frequentProducts,
            "hotdeals":hotdeals,
            "gender_age_recos":gender_age_recos,
            "rts":rts,
            }
        template=loader.get_template("index.html")
        return HttpResponse(template.render( context ,request))
    def post(self,request):
        pass


#회원탈퇴
class DeleteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteView, self).dispatch(request , *args, **kwargs)
    #get방식일때는 페이지만 넘기고 
    def get(self , request):
        template = loader.get_template("delete.html")
        context={}
        return HttpResponse(template.render(context,request))
    #post방식에서 유효성 검사를 해준다.
    def post(self , request):
        #userId를 Cookie에서 갖고온다
        userId = request.session.get("memid")
        #비밀번호를 입력받는다
        passwd = request.POST["passwd"]
        #Member모델에 컬럼이userId와 Cookie안에 memeid의 값이 같다면 
        dto = Member.objects.get(userId = userId)
         
        #비밀번호가 같다면 회원정보를 삭제된 회원 테이블에 넣어준다
        if passwd == dto.passwd :
            deletedto = DeleteMember(
                userId = dto.userId,
                name = dto.name,
                gender = dto.gender,
                address = dto.address,
                detailaddr =dto.address,
                email = dto.email,
                tel = dto.tel,
                signupdate = dto.signupdate 
            )
            # DeleteMember테이블에 탈퇴회원정보를 insert한다
            deletedto.save()
           
            dto.delete()        # member테이블에서 지워준다           
            del(request.session["memid"]) #로그아웃상태로 만들기
            return redirect("member:index")
        else: 
            #비밀번호가 다르면 생기는 페이지
            template = loader.get_template("delete.html")
            context={
                "message" : "비밀번호가 다릅니다.",
                }
            return HttpResponse(template.render(context, request))


#로그아웃을 만들어주는 View    
class LogoutView(View):
    def get (self,request):
        if request.session.get("memid"):
            del(request.session["memid"])
        return redirect("member:index")
    def post(self,request):
        pass

#로그인    
class LoginView(View):
    #post를 사용하기위해 먼저 정의해준다.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request , *args, **kwargs)
    def get(self, request):
        #쿠키에 memid가 있다면
        if request.session.get("memid"):
            #인덱스 페이지로 가라
            return redirect("member:index")
        #쿠키에 memid가 없다면
        else:
            #로그인 페이지그대로 존재
            template=loader.get_template("login.html")
            context={
                }
            return HttpResponse(template.render(context,request))
    def post(self, request):
        #입력받는값
        userId = request.POST["id"]
        passwd = request.POST["passwd"]
        
        #유효성 검사
        try:
            dto = Member.objects.get(userId=userId)
            # passwd가 Member테이블에 있는 것이라면 
            if passwd == dto.passwd:
                request.session["memid"] = userId  #db에있는 userId, passwd가  입력한것이 같다면  session (파이썬에서는 쿠키에)
                #설문지 조사테이블에 아이디가 있다면
                if Answer.objects.filter(userId = userId ):
                    #인덱스페이지로
                    return redirect("member:index")
                else:
                    #아이디가 인덱스페이지에 없다면
                    return redirect("survey:surveylist")
            else:
                message = "비밀번호가 다릅니다"
        except ObjectDoesNotExist:
            message ="아이디가 다릅니다"
            
        template= loader.get_template("login.html")
        
        context = {
            "message" :message
            }
        return HttpResponse(template.render(context, request))
    
#회원가입
class JoinView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JoinView, self).dispatch(request , *args, **kwargs)
    
    # get방식 버튼을 입력할때
    def get(self,request):
        template = loader.get_template("join.html")
        context={
            }
        return HttpResponse(template.render(context,request))
    #입력 데이터 받는곳    
    def post(self,request):
        #templates에서 전화번호를 나눠준것을 받아서
        tel = ""
        tel1 = request.POST["tel1"]
        tel2 = request.POST["tel2"]
        tel3 = request.POST["tel3"]
        #다시 합쳐준다.
        if tel1 and tel2 and tel3 :
            tel = tel1  + "-" + tel2 + "-" + tel3
        email = ""
        email1 = request.POST["email1"]
        email2 = request.POST["email2"]
        if email1 and email2:
            email = email1  + "@" + email2
            
        dto = Member(
           userId = request.POST["id"],
           passwd = request.POST["passwd"],
           name = request.POST["name"],
           age = request.POST["age"],
           gender = request.POST["gender"],
           zonecode = request.POST["zonecode"],
           address = request.POST["addr"],
           detailaddr = request.POST["detailaddr"],
           email = email,
           # 짤라받는곳 붙여 받기
           tel = tel,
           signupdate = DateFormat(datetime.now()).format("Y-m-d") 
        )
        dto.save()
        #setting에서 info 에다 쌓이는것 

        return redirect("member:index") 
    
class IdConfirmView(View):
    def get(self, request):
        userId = request.GET["id"]  
        result = 0
        try :  
            # Member테이블에 아이디가 없다면 userId에 넣어준다
            Member.objects.get(userId=userId)
            # 결과를 일로 받아 준다
            result = 1
        except ObjectDoesNotExist :
            # result = 0 된다면 가입이 안된다. -> idconfirm에서 확인할 수 있다.
            result = 0
        context= {
            "result" : result,
            "userId" : userId
            }

        template =loader.get_template("idconfirm.html")
        return HttpResponse(template.render(context, request))
    
    def post(self, request):  
        pass

class TelConfirmView(View):
    def get(self, request):
        #join.html에서 tel1,tel2,tel3로 나눠진 값들이다
        # 전화번호를 받아준다
        tel = ""
        tel1 = request.GET["tel1"]
        tel2 = request.GET["tel2"]
        tel3 = request.GET["tel3"]

        #-를 포함해서 합쳐준다 tel이라는 변수에 합하기

        if tel1 and tel2 and tel3 :
            tel = tel1  + "-" + tel2 + "-" + tel3 
        result = 0
        try :  
            # 없는 번호라면 값을 넣어준다. 
            Member.objects.get(tel=tel)
            result = 1

        except ObjectDoesNotExist :
            # 있는 번호라면 값을 못넣게 된다 .  telconfirm.html을 확인해본다
            result = 0
            
        context= {
             "result" : result,
             "tel":tel,
             "tel1":tel1,
             "tel2":tel2,
             "tel3":tel3,
             }
    
        template =loader.get_template("telconfirm.html")
        return HttpResponse(template.render(context, request))        
    
    def post(self, request):  
        pass


class MyOrderListView(View):
    def get (self,request):
        template=loader.get_template("myorderlist.html")
        
        userId = request.session.get("memid")
        ordercount = Order.objects.filter(userId=userId).count()

        #페이징
        #pagenum을 get으로 갖고온다
        

        pagenum = request.GET.get( "pagenum" )
        if not pagenum :
            #pagenum은 1로 시작하게 만들기
            pagenum = "1"
        #문자를 숫자로 바꿔준다.    
        pagenum = int(pagenum)
        start = ( pagenum - 1 ) * int(PAGE_SIZE)          # ( 5 - 1 ) * 10 + 1     41 페이지에갖고 올것 처음
        end = start + int(PAGE_SIZE)                      # 41 + 10 - 1            50 페이지에갖고 올것 끝을 정해준다.
        if end > ordercount :
            end = ordercount
            
        orders = Order.objects.filter(userId=userId).order_by("-orderNum")[start:end]
        orderdetaillist = []
        for order in orders:
            refundlist = []
            orderdetails = OrderDetail.objects.filter(orderNum=order.orderNum).order_by("orderDetailNum").values()  # 딕셔너리 여러개가 든 리스트 형태로 반환
            for orderdetail in orderdetails:
                try:
                    refundstatus = Refund.objects.get(orderDetailNum=orderdetail["orderDetailNum"]).status
                except ObjectDoesNotExist:
                    refundstatus = 'x'
                refundlist.append(refundstatus)
            
            orderdetaillist.append(zip(orderdetails, refundlist))
        orderlist = zip(orders, orderdetaillist)
        
        number = ordercount - ( pagenum - 1 ) * int(PAGE_SIZE )
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1       # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0:
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = ordercount // int(PAGE_SIZE)
        if ordercount % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount
        pages = range( startpage, endpage+1 )
        
        context={
            "orderlist" : orderlist,
            "ordercount":ordercount,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            }
        return HttpResponse(template.render(context, request))
    def post(self,request):
        pass
    
class MyOrderDetailView(View):
    def get (self,request):
        template=loader.get_template("myorderdetail.html")
        orderNum = request.GET["orderNum"]
        order = Order.objects.get(orderNum=orderNum)
        memid = request.session.get("memid")
        carts = Cart.objects.filter(userId=memid)
        if order.userId != memid:
            context = {
                "message" : "주문자 정보와 로그인 정보가 일치하지 않습니다.",
                }
            return HttpResponse(template.render( context ,request))
            
        name, tel = Member.objects.filter(userId=memid).values_list("name", "tel")[0]
        orderdetails = OrderDetail.objects.filter(orderNum=orderNum).order_by("orderDetailNum").values()
        
        for orderdetail in orderdetails:
            orderdetail["prodThumbnail"] = Product.objects.get(prodNum=orderdetail["prodNum"]).prodThumbnail
            
        context={
            "carts" : carts,
            "name" : name,
            "tel" : tel,
            "order" : order,
            "orderdetails" : orderdetails,
            }
        return HttpResponse(template.render(context ,request))
    def post(self,request):
        pass
    
class MyBeachView(View):
    def get (self,request):
        memid = request.session.get("memid")
        if memid:
            dto = Member.objects.get(userId=memid)
            context={
                "dto":dto,
                }
        else:
            context = {}
        template=loader.get_template("mybeach.html")
        return HttpResponse(template.render(context ,request))
    def post(self,request):
        pass

##정보수정
class ModifyProView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ModifyProView, self).dispatch(request , *args, **kwargs)
    #여기에는 get방식이 없다.
    def get(self, request):
        pass
    def post(self, request):
        userId = request.session.get("memid")
        dto = Member.objects.get(userId=userId)
        dto.passwd = request.POST["passwd"]
        dto.zonecode = request.POST["zonecode"]
        dto.address = request.POST["addr"]
        dto.detailaddr = request.POST["detailaddr"]
        email = ""
        email1 = request.POST["email1"]
        email2 = request.POST["email2"]
        if email1 and email2:
            email = email1  + "@" + email2
 
        dto.email = email
        dto.save() #insert된다
        return redirect("member:index")
        
        
class ModifyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ModifyView, self).dispatch(request , *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template("modify.html")
        context={}
        return HttpResponse(template.render(context,request))
    def post(self, request):
        userId = request.session.get("memid")
        passwd = request.POST["passwd"]
        dto = Member.objects.get(userId=userId)
        
        if passwd == dto.passwd:
            template = loader.get_template("modifypro.html")
            #여기서 또 짤라준다 dto를 잘라서 template에서 사용하게 만들어준다
            t = dto.tel.split("-")
            if dto.email :
                e = dto.email.split("@")
                context = {
                    "dto" : dto,
                    "t" : t,
                    "e" : e,
                    }
            else:
                context={
                    "dto" : dto
                    }
        else: 
            template=loader.get_template("modify.html")
            context={
                "message" : "비밀번호가 다릅니다." 
                }   
        return HttpResponse(template.render(context,request))

class PapUpView(View):
    def get (self,request):
        context={}
        template=loader.get_template("papup.html")
        return HttpResponse(template.render( context ,request))
    def post(self,request):
        pass