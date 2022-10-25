from product.models import Product
from member.models import Member
from order.models import Order, OrderDetail
import csv
import numpy as np
import pandas as pd
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

def predict_rating(ratings_array, item_similarity):
        sum = ratings_array @ item_similarity   # 행렬곱
        sum_abs = np.array([np.abs(item_similarity).sum(axis=1)])
        return sum / sum_abs

# 안 산 상품 리스트
def no_buy(cart_order_matrix, userId):
    user_buy = cart_order_matrix.loc["id:"+userId, :]   # user 행을 뽑고 열은 전부 가져와라
    no_buy = user_buy[user_buy==0].index.tolist()
    item_list = cart_order_matrix.columns.tolist()
    return [item for item in item_list if item in no_buy]

def recommend(item_pred, userId, no_list, top=10):
    return item_pred.loc["id:"+userId, no_list].sort_values(ascending=False)[:top]

# 장바구니에 들어간 횟수 + 찜목록에 들어간 횟수 + 구매 횟수로 추천
def recommendByCartWishOrder(userId):
    # 협업 필터링
    cart = pd.read_csv("log/cartlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno",
                                                                   "id", "cartNum", "prodNum", "buyCount", "from", "to"])
    cart = cart[["id", "cartNum", "prodNum", "buyCount", "from", "to"]]
    cart_matrix = cart.pivot_table("to", "id", "prodNum", aggfunc="count").fillna(0)
    
    wish = pd.read_csv("log/wishlistlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno",
                                                                       "id", "wishNum", "prodNum", "from", "to"])
    wish = wish[["id", "wishNum", "prodNum", "from", "to"]]
    wish_matrix = wish.pivot_table("to", "id", "prodNum", aggfunc="count").fillna(0)
    
    order = pd.read_csv("log/orderlog.log", encoding="utf-8", names=["asctime", "levelname", "name:lineno",
                                                                     "id", "prodNum", "orderNum", "getterName", "getterTel", "getterZonecode",
                                                                     "getterAddress", "getterDetailAddr", "totalPrice", "from", "to"])
    order = order[["id", "prodNum", "orderNum", "from", "to"]]
    order_matrix = order.pivot_table("orderNum", "id", "prodNum", aggfunc="count").fillna(0)
    
    cart_order = pd.merge(order, cart, on="prodNum")
    cart_order.dropna(axis=0, subset=["orderNum", "prodNum"], inplace=True)
    cart_order_matrix = cart_order.pivot_table(values="orderNum", index="id_x", columns="prodNum", aggfunc="count").fillna(0)
    
    cart_order_matrixT = cart_order_matrix.T    # 사용자 아이디 <-> 상품 번호
    
    cs = cosine_similarity(cart_order_matrixT, cart_order_matrixT)    # 아이템 기반의 유사도 측정 시 코사인 유사도가 주로 쓰인다.
    # print(type(cs)) # numpy.array 타입
    # print(cs) # numpy.array 타입
    similarity = pd.DataFrame(cs, index=cart_order_matrixT.index, columns=cart_order_matrixT.index)
    # print(similarity.head(10))
    
    items = similarity[order['prodNum'][6]].sort_values(ascending=False)[:5]
    # print(items)    # 평점이 유사한 영화들 추천
    
    rating_pred = predict_rating(cart_order_matrix.values, similarity.values)
    rating_df = pd.DataFrame(data=rating_pred, index=cart_order_matrix.index, columns=cart_order_matrix.columns)
    # print(rating_df.head())
    
    # print(cart_order_matrix.columns)
    
    no_buys = no_buy(cart_order_matrix, userId)
    recommend_item = recommend(rating_df, userId, no_buys, 10)
    recommend_df = pd.DataFrame(recommend_item.values, index=recommend_item.index, columns=["predict_score"])
    print("df:",recommend_df)
    
    return recommend_df
    
# # 협업필터링
# def collabfiltering():
#      # 협업시스템
#     prodlog = open("log/shopreview.log", "r", encoding= "utf-8")
#     prods = prodlog.readlines()
#     data=[]
#     for p in prods:
#         logs = p.split(" ")
#         user_id = logs[5].split(":")[1]
#         prodnum = logs[6].split(":")[1]
#         reviewrating = logs[8].split(":")[1]
#         data.append([user_id,prodnum,reviewrating])
#
#     with open("recomprod.csv","w",encoding="utf-8") as f:    
#         f.write("user_id,prodnum,reviewrating\n")
#         for i in data:
#             f.write("{0},{1},{2}\n".format(i[0],i[1],i[2]))
#
#
#
#     df = pd.read_csv("recomprod.csv", sep=",", encoding='utf-8')       
#     df.head()
#     # print()
#     raticngs_matrix = df.pivot_table("reviewrating","user_id","prodnum")
#     raticngs_matrix.fillna(0,inplace=True)
#
#     raticngs_matrix_T= raticngs_matrix.T
#     raticngs_matrix_T.head(3)
#
#     # print(raticngs_matrix_T) #반전
#     item_sim= cosine_similarity(raticngs_matrix_T,raticngs_matrix_T)
#
#     item_sim_df= pd.DataFrame(item_sim, index=raticngs_matrix_T.index,columns=raticngs_matrix_T.index)
#     # print(item_sim)#유사도
#     # print()
#     # print("유사도 데이터 프레임화\n",item_sim_df)#유사도 데이터프레임화
#
#
#     # rerere=item_sim_df[412].sort_values(ascending=False)[1:11]
#     # print()
#     # print("412번의 유사도 상품\n",rerere)
#
#
#
#     #영화추천( 최근접 이웃 협업 필터링)
#     #함수
#     def predict_rating(ratings_arr, item_sim_arr):
#      # ratings_arr: u x i, item_sim_arr: i x i
#         sum_sr = ratings_arr @ item_sim_arr
#         sum_s_abs = np.array([np.abs(item_sim_arr).sum(axis=1)])
#         ratings_pred =  sum_sr / sum_s_abs
#         return ratings_pred
#
#     ratings_pred = predict_rating(raticngs_matrix.values , item_sim_df.values)
#
#     ratings_pred_matrix = pd.DataFrame(data=ratings_pred, index= raticngs_matrix.index,
#                                        columns = raticngs_matrix.columns)
#     ratings_pred_matrix.head(3)
#     # print()
#     # print(ratings_pred_matrix)
#
#     # print("-" *70 ,"\n")
#     # 별점이 있는 실제 영화만 추출(별점 없는건 빼고한다)
#     #(하지만 지금 별점 데이터만 가지고 생성을 해서 이걸하는 의미가 없다 ) )
#
#     # 성능평가하는 MSE를 사용
#     def get_mse(pred, actual):
#         # 평점이 있는 실제 영화만 추출 (1차원 배열로 변환)
#         pred = pred[actual.nonzero()].flatten()
#         actual = actual[actual.nonzero()].flatten()
#
#         return mean_squared_error(pred, actual)
#
#     MSE1 = get_mse(ratings_pred, raticngs_matrix.values)
#     #평균제곱오차 *값이 0에 가까울수록 ㅊ추측한 값이 원본에 가깝기 때문에 0에 가까울수면 정확도가 올라간다.
#     # print(f'아이템 기반 모든 인접 이웃 MSE: {MSE1:.4f}')
#     #
#     # print("-"*80,"\n")
#
#     def predict_rating_topsim(ratings_arr, item_sim_arr, N=20):
#         # 사용자 - 아이템 별점 행렬 크기만큼 0으로 채운 예측 행렬 초기화
#         pred = np.zeros(ratings_arr.shape)
#
#         # 사용자 - 아이템 별점 행렬의 열 크기(아이템 갯수) 만큼 반복 (row: 사용자, col:아이템 )
#         for col in range(ratings_arr.shape[1]):
#
#             # 특정 아이템의 유사도 행렬 오르차순 정렬시에 index ..(1)
#             temp = np.argsort(item_sim_arr[:, col])
#
#             # (1)의 index를 역순으로 나열시 상위 N개의 index = 특정 아이템의 유사도 상위 N개 아이템 index.. (2)
#             top_n_items = [ temp[:-1-N:-1] ]
#
#             # 개인화 된 예측 별점을 계산: 반복당 특정 아이템의 예측 평점(사용자 전체)
#             for row in range(ratings_arr.shape[0]):
#                 # (2)의 유사도 행렬
#                 item_sim_arr_topN=item_sim_arr[col, :][top_n_items].T # N x 1
#                 # (2)의 실제 별점 행렬
#                 ratings_arr_topN =ratings_arr[row, :][top_n_items]
#
#                 # 예측 평점
#                 pred[row, col] = ratings_arr_topN @ item_sim_arr_topN
#                 pred[row, col] /= np.sum( np.abs(item_sim_arr_topN) )
#
#         return pred        
#
#     # 사용자별 예측 별점
#     ratings_pred = predict_rating_topsim(raticngs_matrix.values, item_sim_df.values, N=20)
#
#     #성능평가
#     MSE2 = get_mse(ratings_pred, raticngs_matrix.values)
#     # print(f'아이템 기반 인텀 TOP-20 이웃 MSE: {MSE2:.4f}')
#     # print()
#
#     # 예측 별점 데이터 프레임( 즉 사용자별 예측 별점(ratings_pred를 데이터 프레임화 시키는 코드임.)) 
#     ratings_pred_matrix= pd.DataFrame(data= ratings_pred, index=raticngs_matrix.index,
#                                       columns = raticngs_matrix.columns)
#     # print(ratings_pred_matrix)
#     # print()
#
#     #특정 id가 높은 평점을 준 상품( 실제 별점 )
#     tid="ham" # get.세션(memid) 해줘도 될듯?
#     user_rating_id = raticngs_matrix.loc[tid, :]
#     top_user_rating_id=user_rating_id[ user_rating_id > 0 ].sort_values(ascending=False)[:10]
#     # print("id: {0}가 높은 별점을 준 상품\n{1}".format(tid,top_user_rating_id))
#     # for topdata in top_user_rating_id:
#     #     print(topdata)
#
#
#     # 특정 id가 아직 별점을 주지 않은 상품추천 (특정 id가 아직 안본 상품의 추천)
#     def get_unseen_prod(raticngs_matrix, userId):
#
#         # user_rating: userId의 아이템 평점 정보 ( 시리즈 형태: prod번호를 index로 가진다.)
#         user_rating = raticngs_matrix.loc[userId,:]
#
#         # user_rating = 0인 아직 안본 상품
#         unseen_prod_list = user_rating[ user_rating == 0].index.tolist()
#
#         # 모든 상품번호를 list객체로 변환
#         prod_list = raticngs_matrix.columns.tolist()
#
#         # 한줄 for + if문으로 안본 영화 리스트 생성
#         unseen_list= [ prod for prod in prod_list if prod in unseen_prod_list ]
#
#         return unseen_list
#
#     # 보지 않은 영화 중에 예측 높은 순서로 시리즈 반환
#     def recomm_prod_by_userid(pred_df, userId, unseen_list, top_n=10):
#         recomm_prod = pred_df.loc[userId, unseen_list].sort_values(ascending=False)[:top_n]
#
#         return recomm_prod
#
#     ######
#     # 아직 보지 않은 상품 리스트
#     target_id="ham"
#     unseen_list = get_unseen_prod(raticngs_matrix, target_id) # 0~9 총10개 뽑아라
#
#     # 아이템 기반의 최근접 이웃 협업 필터링으로 상품 추천
#     recomm_prods= recomm_prod_by_userid(ratings_pred_matrix, target_id, unseen_list, top_n=10)
#                                         # 예측 별점 데이터 프레임    id        안본 리스트    가장위10개
#
#     # 데이터 프레임 생성
#     df_recomm_prods =pd.DataFrame(data=recomm_prods.values, index=recomm_prods.index, columns=["pred_score"])
#
#     # print()
#     # print(recomm_prods*100)
#     # print("\n 아이템기반의 최근접 이웃 협업 필터링으로 만든 상품추천\n",df_recomm_prods)
#
#     # print()
#     pdlists=[]
#     chl = df_recomm_prods.index
#     for ii in chl:
#         pdlist = Shopproduct.objects.get(prodnum=ii)
#         pdlists.append(pdlist)
#
#
#     print(pdlists)