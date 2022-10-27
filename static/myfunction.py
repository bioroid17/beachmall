from product.models import Product
from member.models import Member
from order.models import Order, OrderDetail
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
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



# 실시간 검색어
def realtimeSearch():
    # 실시간 검색어 출력
    searchrank = pd.read_csv("log/searchlog.log", encoding='utf-8', names=["asctime", "levelname", "name:lineno", "id", "query", "pagenum", "from", "to"]) # 저장한 csv 읽기
    
    sl = searchrank.groupby('query')['query'].count().reset_index(name='count') # 그룹으로 묶은것들의 갯수를 샌다음 count라는 칼럼명을 지정해줌
    slh = sl.sort_values(by='count', ascending=False).head(10) # 위부터 10개만 뽑음
    slr = slh.reset_index(drop=True) # 기존의 index 테이블 삭제
    return [row.split(":")[1] for row in slr["query"]]


def predict_item(item_array, item_similarity):
        sum = item_array @ item_similarity   # 행렬곱
        sum_abs = np.array([np.abs(item_similarity).sum(axis=1)])
        return sum / sum_abs

# 안 산 상품 리스트
def no_buy(cart_order_matrix, user):
    user_buy = cart_order_matrix.loc[user, :]   # user 행을 뽑고 열은 전부 가져와라
    no_buy = user_buy[user_buy==0].index.tolist()
    item_list = cart_order_matrix.columns.tolist()
    return [item for item in item_list if item in no_buy]

def recommend(item_pred, user, no_list, top=10):
    return item_pred.loc[user, no_list].sort_values(ascending=False)[:top]

# 장바구니에 들어간 횟수 + 찜목록에 들어간 횟수 + 구매 횟수로 추천
def recommendByCartWishOrder(userId):
    # 협업 필터링
    cart = pd.read_csv("csvs/cartcsv.csv", encoding="utf-8", header=0)
    cart.dropna(axis=0, subset=["prodNum"], inplace=True)
    cart_matrix = cart.pivot_table("to", "id", "prodNum", aggfunc="count").fillna(0)
    
    wish = pd.read_csv("csvs/wishlistcsv.csv", encoding="utf-8", header=0)
    wish.dropna(axis=0, subset=["prodNum"], inplace=True)
    wish_matrix = wish.pivot_table("to", "id", "prodNum", aggfunc="count").fillna(0)
    
    order = pd.read_csv("csvs/ordercsv.csv", encoding="utf-8", header=0)
    order.dropna(axis=0, subset=["prodNum"], inplace=True)
    order_matrix = order.pivot_table("orderNum", "id", "prodNum", aggfunc="count").fillna(0)
    
    cart_order = pd.merge(order, cart, on="prodNum")
    cart_order.dropna(axis=0, subset=["orderNum", "prodNum"], inplace=True)
    cart_order_matrix = cart_order.pivot_table(values="orderNum", index="id_x", columns="prodNum", aggfunc="count").fillna(0)
    
    cart_order_matrixT = cart_order_matrix.T    # 사용자 아이디 <-> 상품 번호
    
    cs = cosine_similarity(cart_order_matrixT, cart_order_matrixT)    # 아이템 기반의 유사도 측정 시 코사인 유사도가 주로 쓰인다.
    # print(type(cs)) # numpy.array 타입
    # print(cs) # numpy.array 타입
    similarity = pd.DataFrame(cs, index=cart_order_matrixT.index, columns=cart_order_matrixT.index)
    
    # orderNum = Order.objects.filter(userId=userId).order_by("-orderNum").first().orderNum
    # linenum = order[order["orderNum"]==orderNum].index[-1]
    
    # items = similarity[order['prodNum'][linenum]].sort_values(ascending=False)
    # print(items)    # 평점이 유사한 영화들 추천
    
    item_pred = predict_item(cart_order_matrix.values, similarity.values)
    item_df = pd.DataFrame(data=item_pred, index=cart_order_matrix.index, columns=cart_order_matrix.columns)
    
    no_buys = no_buy(cart_order_matrix, userId)
    recommend_item = recommend(item_df, userId, no_buys, 10)
    recommend_df = pd.DataFrame(recommend_item.values, index=recommend_item.index, columns=["predict_score"])
    # print(recommend_df)
    
    return recommend_df

# 성별과 연령대로 추천
def gender_age_recommend(userId):
    # 협업 필터링
    user = Member.objects.get(userId=userId)
    user_gender_age = user.gender +"_"+ user.age
    # 장바구니
    cartlog = open("log/cartlog.log", 'r', encoding="utf-8")
    cartcsv = open("csvs/cartcsv.csv", 'w', encoding="utf-8", newline="")
    cartlines = csv.reader(cartlog)
    cartwr = csv.writer(cartcsv)
    cartwr.writerow(["id", "gender_age", "prodNum", "buyCount", "from", "to"])
    for line in cartlines:
        if line[8].startswith("to:/cart/cartins") == False:
            continue
        member = Member.objects.get(userId=line[3].split(":")[1])
        cartwr.writerow([line[3].split(":")[1], member.gender+"_"+member.age, line[5].split(":")[1],
                         line[6].split(":")[1], line[7].split(":")[3], line[8].split(":")[1]])
    cartlog.close()
    cartcsv.close()
    cart = pd.read_csv("csvs/cartcsv.csv", encoding="utf-8", header=0)
    cart.dropna(axis=0, subset=["prodNum"], inplace=True)
    cart_matrix = cart.pivot_table("to", "gender_age", "prodNum", aggfunc="count").fillna(0)
    
    # 찜 목록
    wishlog = open("log/wishlistlog.log", 'r', encoding="utf-8")
    wishcsv = open("csvs/wishlistcsv.csv", 'w', encoding="utf-8", newline="")
    wishlines = csv.reader(wishlog)
    wishwr = csv.writer(wishcsv)
    wishwr.writerow(["id", "gender_age", "prodNum", "from", "to"])
    for line in wishlines:
        if line[7].startswith("to:/wishlist/wishins") == False:
            continue
        member = Member.objects.get(userId=line[3].split(":")[1])
        wishwr.writerow([line[3].split(":")[1], member.gender+"_"+member.age, line[5].split(":")[1], line[6].split(":")[3], line[7].split(":")[1]])
    wishlog.close()
    wishcsv.close()
    wish = pd.read_csv("csvs/wishlistcsv.csv", encoding="utf-8", header=0)
    wish.dropna(axis=0, subset=["prodNum"], inplace=True)
    wish_matrix = wish.pivot_table("to", "gender_age", "prodNum", aggfunc="count").fillna(0)
    
    # 주문 목록
    orderlog = open("log/orderlog.log", 'r', encoding="utf-8")
    ordercsv = open("csvs/ordercsv.csv", 'w', encoding="utf-8", newline="")
    orderlines = csv.reader(orderlog)
    orderwr = csv.writer(ordercsv)
    orderwr.writerow(["id", "gender_age", "prodNum", "orderNum", "from", "to"])
    for line in orderlines:
        if "" in line:
            continue
        member = Member.objects.get(userId=line[3].split(":")[1])
        orderwr.writerow([line[3].split(":")[1], member.gender+"_"+member.age, line[4].split(":")[1],
                         line[5].split(":")[1], line[12].split(":")[3], line[13].split(":")[1]])
    orderlog.close()
    ordercsv.close()
    order = pd.read_csv("csvs/ordercsv.csv", encoding="utf-8", header=0)
    order.dropna(axis=0, subset=["prodNum"], inplace=True)
    order_matrix = order.pivot_table("orderNum", "gender_age", "prodNum", aggfunc="count").fillna(0)
    
    cart_order = pd.merge(order, cart, on="prodNum")
    cart_order.dropna(axis=0, subset=["orderNum", "prodNum"], inplace=True)
    cart_order_matrix = cart_order.pivot_table(values="orderNum", index="gender_age_x", columns="prodNum", aggfunc="count").fillna(0)
    
    cart_order_matrixT = cart_order_matrix.T    # 사용자 아이디 <-> 상품 번호
    
    cs = cosine_similarity(cart_order_matrixT, cart_order_matrixT)    # 아이템 기반의 유사도 측정 시 코사인 유사도가 주로 쓰인다.
    
    similarity = pd.DataFrame(cs, index=cart_order_matrixT.index, columns=cart_order_matrixT.index)
    # print(similarity.head(10))
    
    # linenum = order[order["gender_age"]==user_gender_age].index[-1]
    # print(linenum)
    
    # items = similarity[order['prodNum'][linenum]].sort_values(ascending=False)
    # print(items)    # 추천 상품
    
    item_pred = predict_item(cart_order_matrix.values, similarity.values)
    item_df = pd.DataFrame(data=item_pred, index=cart_order_matrix.index, columns=cart_order_matrix.columns)
    
    no_buys = no_buy(cart_order_matrix, user_gender_age)
    recommend_item = recommend(item_df, user_gender_age, no_buys, 10)
    recommend_df = pd.DataFrame(recommend_item.values, index=recommend_item.index, columns=["predict_score"])
    # print(str(list(recommend_df.index)))
    
    return recommend_df
