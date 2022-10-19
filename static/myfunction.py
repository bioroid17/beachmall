from product.models import Product
from member.models import Member
from order.models import Order, OrderDetail
import csv
import numpy as np
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
    # print(searchrank)
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

# 장바구니에 들어간 횟수 + 찜목록에 들어간 횟수 + 구매 횟수로 추천
def recommendByCartWishOrder():
    # 협업 필터링
    cart = pd.read_csv("log/cartlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno",
                                                                   "id", "cartNum", "prodNum", "buyCount", "from", "to"])
    cart = cart[["id", "cartNum", "prodNum", "buyCount", "from", "to"]]
    print(cart)
    wish = pd.read_csv("log/wishlistlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno",
                                                                       "id", "wishNum", "prodNum", "from", "to"])
    wish = wish[["id", "wishNum", "prodNum", "from", "to"]]
    print(wish)
    order = pd.read_csv("log/orderlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno", "id", "orderNum", "getterName", "getterTel",
                                                                     "getterZonecode", "getterAddress", "getterDetailAddr", "totalPrice", "from", "to"])
    order = order[["id", "orderNum", "getterName", "getterTel", "getterZonecode", "getterAddress", "getterDetailAddr", "totalPrice", "from", "to"]]
    print(order)
    
    cart.fillna(0, inplace=True)
    wish.fillna(0, inplace=True)
    order.fillna(0, inplace=True)
    
    cart_order = pd.merge(order, cart, on="id")
    print(cart_order.head())
    # ratings_movie = pd.merge(ratings, movies, on="movieId")  # ratings를 기준으로 movies를 join
    # # print(ratings_movie.head())
    
    cart_order_matrix = cart_order.pivot_table(index="prodNum", columns="id", values="orderNum", aggfunc="count")
    print(cart_order_matrix.head())
    # ratings_matrix = ratings_movie.pivot_table("rating", "userId", "title")
    # # print(ratings_matrix.head())
    
    
    # ratings_matrix.fillna(0, inplace=True)
    # # print(ratings_matrix.shape)        # (610, 9719)
    
    
    # ratings_matrixT = ratings_matrix.T  # 사용자 아이디 <-> 영화 아이디
    #
    
    # from sklearn.metrics.pairwise import cosine_similarity      # 코사인 유사도
    # cs = cosine_similarity(ratings_matrixT, ratings_matrixT)    # 아이템 기반의 유사도 측정 시 코사인 유사도가 주로 쓰인다.
    # # print(type(cs)) # numpy.array 타입
    # similarity = pd.DataFrame(cs, index=ratings_matrixT.index, columns=ratings_matrixT.index)
    # # print(similarity.head(1))
    #
    # items = similarity[movies['title'][300]].sort_values(ascending=False)[:5]
    # # print(items)    # 평점이 유사한 영화들 추천
    #
    # def predict_rating(ratings_array, item_similarity):
    #     sum = ratings_array @ item_similarity   # 행렬곱
    #     sum_abs = np.array([np.abs(item_similarity).sum(axis=1)])
    #     return sum / sum_abs
    #
    # rating_pred = predict_rating(ratings_matrix.values, similarity.values)
    # rating_df = pd.DataFrame(data=rating_pred, index=ratings_matrix.index, columns=ratings_matrix.columns)
    # # print(rating_df.head())
    #
    # # print(ratings_matrix.columns)
    #
    # # 안 본 영화 리스트
    # def no_watch(ratings_matrix, user):
    #     user_rating = ratings_matrix.loc[user, :]   # user 행을 뽑고 열은 전부 가져와라
    #     no_watching = user_rating[user_rating==0].index.tolist()
    #     movie_list = ratings_matrix.columns.tolist()
    #     return [movie for movie in movie_list if movie in no_watching]
    #
    # def recommend(rating_pred, userId, no_list, top=10):
    #     return rating_pred.loc[userId, no_list].sort_values(ascending=False)[:top]
    #
    # userId = 15
    # no_watching = no_watch(ratings_matrix, userId)
    # recommend_movie = recommend(rating_df, userId, no_watching, 10)
    # recommend_df = pd.DataFrame(recommend_movie.values, index=recommend_movie.index, columns=["predict_score"])
    # print(recommend_df)