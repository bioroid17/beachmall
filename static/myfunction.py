from product.models import Product
from member.models import Member
from order.models import Order, OrderDetail
import csv
import pandas as pd

"""
직접 정의한 함수들은 여기에 직접 작성해서 쓴다.
"""

# 최근 본 상품
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

# 성별과 연령대로 추천
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
    
    reco_sorted = [(key, value) for key, value in recommends.items()]
    print(reco_sorted, len(reco_sorted))
    if len(reco_sorted) > 0:
        reco_sorted.sort(key=lambda x:x[1], reverse=True)
    
    return reco_sorted[0:6]

# 실시간 검색어
def realtimeSearch():
    # 실시간 검색어 출력
    searchrank = pd.read_csv("log/searchlog.log", encoding='utf-8', names=["asctime", "levelname", "name:lineno", "id", "query", "pagenum", "from", "to"]) # 저장한 csv 읽기
    print(searchrank)
    sl = searchrank.groupby('query')['query'].count().reset_index(name='count') # 그룹으로 묶은것들의 갯수를 샌다음 count라는 칼럼명을 지정해줌
    slh = sl.sort_values(by='count', ascending=False).head(10) # 위부터 10개만 뽑음
    slr = slh.reset_index(drop=True) # 기존의 index 테이블 삭제
    return [row.split(":")[1] for row in slr["query"]]

# 고객이 한번 구매한 상품을 다시 구매한다.
def buyAgain(userId):
    buylist = []
    orders = Order.objects.filter(userId=userId)
    for order in orders:
        orderDetails = OrderDetail.objects.filter(orderNum=order.orderNum.orderNum)
        # for

# 설문조사 받은 내용으로 적용할 것
def recommendBySurvey():
    pass