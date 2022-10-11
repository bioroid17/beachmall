from product.models import Product

def getRecentProduct(userId):
    
    productlog = open("log/productlog.log", 'r', encoding="utf-8")
    lines = productlog.readlines()[::-1]
    
    recents = []
    count = 0
    for line in lines:
        if count >= 4:
            break
        else:
            logs = line.split(",")
            id = logs[3].split(":")[1]
            if id != userId:
                continue
            prodNum = logs[4].split(":")[1]
            if Product.objects.filter(prodNum=prodNum).count() == 0:
                continue
            if prodNum not in recents:
                recents.append(prodNum)
                count += 1
    recentProducts = [Product.objects.get(prodNum=recent) for recent in recents]
    
    productlog.close()
    
    return recentProducts