from django.shortcuts import render
from django.db.models import Q
from product.models import Product
import logging

PAGE_SIZE = 30
PAGE_BLOCK = 3

# Create your views here.

logger = logging.getLogger(__name__)

def searchResult(request):
    query = request.GET.get('kw')
    
    count = Product.objects.all().filter(
        Q(prodName__icontains=query)|
        Q(brand__icontains=query)
    ).count()
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int(pagenum)
    
    start = (pagenum - 1) * int(PAGE_SIZE)      # (5 - 1) * 10    = 40    슬라이싱을 위해 0~10까지 잡기
    end = start + int(PAGE_SIZE)                # 40 + 10         = 50
    if end > count :
        end = count
    dtos = Product.objects.all().filter(
        Q(prodName__icontains=query)|
        Q(brand__icontains=query)
    )[start:end]
    number = count - (pagenum - 1) * int(PAGE_SIZE)
    
    startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1    # 9 // 10 * 10 + 1     = 1
    if pagenum % int(PAGE_BLOCK) == 0:
        startpage -= int(PAGE_BLOCK)
    endpage = startpage + int(PAGE_BLOCK) - 1                       # 1 + 10 - 1           = 10
    pagecount = count // int(PAGE_SIZE)
    if count % int(PAGE_SIZE) > 0 :
        pagecount += 1
    if endpage > pagecount:
        endpage = pagecount
    pages = range(startpage, endpage + 1)
    
    context = {
        'query':query,
        'dtos':dtos,
        "count" : count,
        "pagenum" : pagenum,
        "number" : number,
        "pages" : pages,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount
        }
    memid = request.session.get("memid")
    if memid:
        logger.info("id:"+memid+",query:"+query+",pagenum:"+pagenum+",from:"+request.META["HTTP_REFERER"]+",to:"+request.get_full_path())
    return render(request,'search.html', context)    