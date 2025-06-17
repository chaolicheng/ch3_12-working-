from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def search_list(request):
    if "cName" in request.GET:
        cName=request.GET["cName"]
        print(cName)
        # resultList=students.objects.filter(cName=cName)
        resultList=students.objects.filter(cName__contains=cName)
    else:
        resultList=students.objects.all()

    erroe_message=""
    if not resultList:
        erroe_message="無此資料"

    # for data in resultList:
    #     print(model_to_dict(data))

    # return HttpResponse("hello")

    return render(request, "search_list.html", locals())

def index(request):
    if "site_search" in request.GET:
        site_search=request.GET["site_search"]
        site_search=site_search.strip() #去除前後空白
        print(site_search)
        #一個關鍵字 搜尋一個欄位
        # resultList=students.objects.filter(cName__contains=site_search)

        #一個關鍵字 搜尋多個欄位
        # resultList=students.objects.filter(
        #     Q(cName__contains=site_search)|
        #     Q(cBirthday__contains=site_search)|
        #     Q(cEmail__contains=site_search)|
        #     Q(cPhone__contains=site_search)|
        #     Q(cAddr__contains=site_search)
        # )

        #多個關鍵字 搜尋多個欄位
        keyworks=site_search.split() #切割
        print(keyworks)
        # resultList=[]
        q_object=Q()
        for keywork in keyworks:
            q_object.add(Q(cName__contains=keywork), Q.OR)
            q_object.add(Q(cBirthday__contains=keywork), Q.OR)
            q_object.add(Q(cEmail__contains=keywork), Q.OR)
            q_object.add(Q(cPhone__contains=keywork), Q.OR)
            q_object.add(Q(cAddr__contains=keywork), Q.OR)
        resultList=students.objects.filter(q_object)
    else:
        resultList=students.objects.all().order_by("cID")
    
    dataCount=len(resultList)
    status=True
    error_message=""
    if not resultList:
        status=False
        error_message="無此資料"
    #分頁設定，每頁顯示三筆
    paginator=Paginator(resultList, 3)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number) #根據取得page_number，得到對應頁數的資料
    #page_obj 包含該頁資料的物件
    #page_obj.object_list 該頁的資料
    #page_obj.has_next, page_obj.has_previous 是否有下一頁或上一頁
    #page_obj.next_page_number, page_obj.previous_page_number 下一頁或上一頁的頁數
    #page_obj.number 當前頁數
    #paginator.num_pages 總頁數

    # print(dataCount)
    return render(request, "index.html", locals())

def post(request):
    if request.method=="POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName={cName}, cSex={cSex}, cBirthday={cBirthday}, cEmail={cEmail}, cPhone={cPhone}, cAddr={cAddr}")
        #orm
        add=students(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail, cPhone=cPhone, cAddr=cAddr)
        add.save()
        # return HttpResponse("hello")
        return redirect("/index/")
    else:
        return render(request, "post.html", locals())