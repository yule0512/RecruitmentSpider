
from django.shortcuts import render

#引入类
from myweb.models import Jobs

from django.http import HttpResponse

#数据库or查询
from django.db.models import Q

#分页需要模块
from django.core.paginator import Paginator

#===============视图方法==============================

#首页视图方法
def loadContent(request):
    content={}
    content['typeslist'] = Jobs.objects.all()
    return content

def pos_index(request,pIndex):
    #所有职位
    kw = 'position'
    lists = Jobs.objects.all()[:150]
    p = Paginator(lists,15)
    #处理当前页号信息
    if pIndex == "":
        pIndex = '1'
    pIndex = int(pIndex)
     #获取当前页数据
    lists2 = p.page(pIndex)
    plist = p.page_range
    # 下拉--月薪
    context = {'poslists':lists2,'pIndex':pIndex,'plist':plist,'kw':kw}
    return render(request,'index.html',context)

#检索展示页面
def pos_list(request,pIndex):
    ge = ''
    gl = ''
    kw = 'position'
    lists = Jobs.objects.filter()
    if  request.GET['edu']  != '':
        print ('edu')
        ge = request.GET['edu']
        lists = Jobs.objects.filter( Q(edu__contains = ge))
    try:
        if request.GET['position'] != '':
            print ('posi')
            kw = 'position'
            gl = request.GET['position']
            lists = lists.filter(Q(name__contains = gl) | Q(info__contains = gl ))
    except:
        if request.GET['company'] != '':
            kw = 'company'
            gl = request.GET['company']
            lists = lists.filter(co_name__contains = gl)
    lists = lists[:150]
    p = Paginator(lists,15)
    #处理当前页号信息
    if pIndex == "":
        pIndex = '1'
    pIndex = int(pIndex)
     #获取当前页数据
    lists2 = p.page(pIndex)
    plist = p.page_range
    # 下拉--月薪
    context = {'poslists':lists2,'pIndex':pIndex,'plist':plist,'gl':gl,'ge':ge,'kw':kw}
    return render(request,'index.html',context)


#详情页面
def pos_detail(request,gd):
    content = loadContent(request)
    posb = Jobs.objects.get(id = gd)
    content['pos'] = posb
    return render(request,'job_detail.html',content)
