from datetime import datetime
from static.myfunction import recommendByCartWishOrder, gender_age_recommend
from member.models import Member
from recommend.models import Recommend
def schedule_api():
    print("%s에 실행됨." % datetime.now())
    users = Member.objects.all()
    for user in users:
        try:
            cart_wish_order_recos = str(list(recommendByCartWishOrder(user.userId).index))
            gender_age_recos = str(list(gender_age_recommend(user.userId).index))
            reco1 = Recommend(
                userId = user.userId,
                prodList = cart_wish_order_recos,
                status = "cart_wish_order"
                )
            reco2 = Recommend(
                userId = user.userId,
                prodList = gender_age_recos,
                status = "gender_age"
                )
            reco1.save()
            reco2.save()
            print("%s 저장 완료" % user.userId)
        except Exception:
            print("%s 저장 실패" % user.userId)
            continue
    print("추천 저장 완료")