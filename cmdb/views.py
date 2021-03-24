from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from  django.http import HttpResponse

from .encapsulation_request import *
# Create your views here.
from . import models
import json

def detail_data(request):

    nid=request.GET.get('nid')
    # print(nid)
    if request.method=='GET':
        detail =models.select_detail(nid)
        # print('detail:',detail)

        return render(request,'detail_page.html',{'detail':detail})
    elif request.method=='POST':
        pass

def update_data(request):#修改数据

    if request.method=='GET':
        nid = request.GET.get('nid',None)
        detail =models.select_detail(nid)
        print('detail:',detail)
        return render(request,'modify_page.html',{'detail':detail})
    elif request.method=='POST':
        id=request.POST.get('id',None)
        api_url = request.POST.get('api_url', None)
        api_header = request.POST.get('api_header', None)
        api_method = request.POST.get('api_method', None)
        api_name = request.POST.get('api_name', None)
        api_data = request.POST.get('api_data', None)
        # print('更改详情信息')
        # print('更改详情信息:',id,api_url,api_header,api_method,api_name,api_data)
        # api_header = json.dumps(api_header)
        # api_data = json.dumps(api_data)
        detail= models.update_data(id,api_url,api_header,api_method,api_name,api_data)
        # print('detail:',detail)
        return render(request, 'modify_page.html',{'detail':detail})
def delete_data(request):#删除数据
    id = request.GET.get('nid',None)
    print(id)
    # 调用删除
    models.delete_data(id)

    return redirect('/page/main/select/')

def select_data(request):#查询数据

    if request.method=='POST':
        api_name = request.POST.get('api_name', None)
        project = request.POST.get('project', None)
        create_user = request.POST.get('create_user', None)
        data = models.select_data(api_name,project,create_user)
        print(api_name,project,create_user)
        print('数据汇总:',data)

        return render(request, 'home_page.html', {'data': data},)
    elif  request.method=='GET':
        api_name = request.GET.get('api_name', None)
        project = request.GET.get('project', None)
        create_user = request.GET.get('create_user', None)
        data = models.select_data(api_name,project,create_user)
        return render(request, 'home_page.html', {'data': data},)


def page(request):#新增接口数据
    if request.method =='GET':
        return render(request, 'home_page.html')
    elif request.method=='POST':
        data=''

        if request.POST.get('operation_name', None) == 'add':
            project = request.POST.get('project', None)
            project_name = request.POST.get('project_name', None)
            url = request.POST.get('url', None)
            data = request.POST.get('data', None)
            header = request.POST.get('header', None)
            method = request.POST.get('method', None)
            #转义成json格式
            # data = json.dumps(data)
            # header = json.dumps(header)

            models.add_data(project,project_name,url,data,header,method)
            return render(request, 'home_page.html')
        elif request.POST.get('operation_name', None) == 'select':
            # api_name = request.POST.get('api_name', None)
            # project = request.POST.get('project', None)
            # create_user = request.POST.get('create_user', None)
            # data = models.select_data(api_name,project,create_user)
            # data=data
            # print(type(data),data)
            # msg = {'msg': data}
            # print(msg,type(msg))
            # print(msg['msg'][0])
            # data = [{'id': 5, 'project': '1', 'api_name': '1', 'api_url': '1', 'api_data': '1', 'api_header': '1',
            #             'api_method': '1', 'api_response': None, 'create_time': '2021-03-18 14:33:53',
            #             'modify_time': '2021-03-18 14:33:53', 'modify_user_code': None}]
            # return render(request, 'detail_page.html', {'data': data})
            pass
        else:
            pass

        # return render(request, 'home_page.html',locals())
                      # {'data': data})


    else:
        pass

def execute_data(request):#执行API请求
    id = request.GET.get('nid',None)
    # print(id)
    database_result = models.select_detail(id)
    # print(type(database_result[0]))
    api_url = database_result[0]['api_url']
    api_data = database_result[0]['api_data']
    api_header = database_result[0]['api_header']
    api_method = database_result[0]['api_method']

    headers = json.loads(api_header)#该requestsAPI明确规定，headers必须是一个字典：

    result = RunMain(url=api_url,data=api_data,method=api_method,headers=headers)
    print(result.result,result.code)
    response = result.result
    code = result.code
    # response= json.dumps(response)
    models.update_api_data(id,response,code)
    return redirect('/page/main/select/')
