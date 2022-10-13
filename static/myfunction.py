from product.models import Product
import csv
from member.models import Member
from order.models import Order, OrderDetail

def getRecentProduct(userId):
    
    productlog = open("log/productlog.log", 'r', encoding="utf-8")
    lines = csv.reader(productlog)
    
    recents = []
    count = 0
    for line in reversed(list(lines)):
        if count >= 4:
            break
        else:
            id = line[3].split(":")[1]
            if id != userId:
                continue
            if line[4] == "" or line[4] == None:
                continue
            prodNum = line[4].split(":")[1]
            if Product.objects.filter(prodNum=prodNum).count() == 0:
                continue
            if prodNum not in recents:
                recents.append(prodNum)
                count += 1
    recentProducts = [Product.objects.get(prodNum=recent) for recent in recents]
    
    productlog.close()
    
    return recentProducts

def recommendByGenderAge(userId):
    member = Member.objects.get(userId=userId)
    gender = member.gender
    age = member.age

    reco_members = Member.objects.filter(age=age).filter(gender=gender)
    
    recommends = {}
    
    for reco_member in reco_members:
        orders = Order.objects.filter(userId=reco_member.userId)
        for order in orders:
            orderDetails = OrderDetail.objects.filter(orderNum=order.orderNum)
            for orderDetail in orderDetails:
                if str(orderDetail.prodNum) in recommends:
                    recommends[str(orderDetail.prodNum)] += 1
                else:
                    recommends[str(orderDetail.prodNum)] = 1