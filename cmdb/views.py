from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from  django.http import HttpResponse

from .encapsulation_request import *
# Create your views here.
from . import models
import json
import time

def detail_data(request):#查询明细

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
        print('更改详情信息')
        print('更改详情信息:',api_name)

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
        print(request.POST.get('operation_name', None))

        if request.POST.get('operation_name', None) == 'add':
            project = request.POST.get('project_add', None)
            project_name = request.POST.get('project_name_add', None)
            url = request.POST.get('url_add', None)
            data = request.POST.get('data_add', None)
            header = request.POST.get('header_add', None)
            method = request.POST.get('method_add', None)
            #转义成json格式
            # data = json.dumps(data)
            # header = json.dumps(header)

            models.add_data(project,project_name,url,data,header,method)
            return render(request, 'home_page.html')

        else:
            return render(request, 'home_page.html')


def execute_data(request):#执行API请求
    id = request.GET.get('nid',None)
    # print(id)
    database_result = models.select_detail(id)
    # print(type(database_result[0]))
    api_url = database_result[0]['api_url']
    api_data = database_result[0]['api_data']
    api_header = database_result[0]['api_header']
    api_method = database_result[0]['api_method']
    print('api_header',api_header)
    headers = json.loads(api_header)#该requestsAPI明确规定，headers必须是一个字典：

    result = RunMain(url=api_url,data=api_data,method=api_method,headers=headers)
    print(result.result,result.code)
    response = result.result
    response=response.get('lastmileLabel',None)
    print('response:',response)
    code = result.code
    print(code)
    # response= json.dumps(response)
    models.update_api_data(id,response,code)
    return redirect('/page/main/select/')

def Associated_api(request):#API关联关系

    # print(request.method)
    if request.method=='GET':
        data = models.select_data()
        return render(request,'Associated_api1.html',{'data': data},)
    elif request.method=='POST':
        print(request.POST.get('name',None))
        values= request.POST.get('name',None)

        if values=='select':
            select = models.select_Associated_api()
            return  render(request,'Associated_api1.html',{'select': select},)
        elif values == 'add_data':
            logic_name = request.POST.get('logic_name',None)
            logic_project = request.POST.get('logic_project',None)
            api_name = request.POST.getlist('api_name',None)
            next_api_name = request.POST.getlist('next_api_name',None)
            extraction_type1 = request.POST.getlist('extraction_type1',None)
            order_desc= request.POST.getlist('order_desc',None)
            extraction_type2= request.POST.getlist('extraction_type2',None)
            assignment_name1 = request.POST.getlist('assignment_name1',None)
            assignment_name2 = request.POST.getlist('assignment_name2',None)

            data_dict= models.add_Associated_api(logic_project,logic_name)
            print(data_dict)
            Associated_id = data_dict[0]['id']
            Associated_name = data_dict[0]['Associated_name']
            # print('api_name:',api_name,'next_api_name',next_api_name,'extraction_type1:',extraction_type1,'order_desc:',order_desc,'extraction_type2:',extraction_type2,'assignment_name1:',assignment_name1,'assignment_name2:',assignment_name2)

            #定义循环次数
            frequency = int(len(order_desc))
            for i in  range(frequency):

                print('try  ')
                if i >0:
                    print(Associated_id, Associated_name, api_name[i], next_api_name[i], extraction_type1[i],
                          extraction_type2[i - 1], order_desc[i], assignment_name1[i], assignment_name2[i-1])
                    models.add_Associated_api_detail(Associated_id=Associated_id,Associated_name=Associated_name,
                                                     api_name=api_name[i], next_api_name=next_api_name[i],
                                                     extraction_type1=extraction_type1[i],
                                                     order_desc=order_desc[i], assignment_name1=assignment_name1[i],
                                                     assignment_name2=assignment_name2[i-1],extraction_type2=extraction_type2[i - 1]
                                                     )
                else:
                    print(Associated_id, Associated_name, api_name[i], next_api_name[i], extraction_type1[i]
                          , order_desc[i], assignment_name1[i])
                    models.add_Associated_api_detail(Associated_id=Associated_id, Associated_name=Associated_name,
                                                     api_name=api_name[i], next_api_name=next_api_name[i],
                                                     extraction_type1=extraction_type1[i],
                                                     order_desc=order_desc[i], assignment_name1=assignment_name1[i])

            return render(request, 'Associated_api1.html')





    else:
        pass

def login(request):

    return render(request,'login.html')

def Associated_api_detail(request):
    api_associated_id= request.GET.get('nid',None)
    detail_data=models.Associated_api_detail(api_associated_id)
    return  render(request,'Associated_api_detail.html',{'detail_data':detail_data})

def Associated_api_modify(request):
    if request.method =='GET':
        api_associated_id = request.GET.get('nid', None)
        detail_data = models.Associated_api_detail(api_associated_id)
        option_data = models.select_data()
        return render(request, 'Associated_api_modify.html', {'detail_data': detail_data,'option_data':option_data})
    elif request.method =='POST':
        api_name = request.POST.getlist('api_name', None)
        next_api_name = request.POST.getlist('next_api_name', None)
        order_desc = request.POST.getlist('order_desc', None)
        extraction_type1 = request.POST.getlist('extraction_type0', None)
        extraction_type2 = request.POST.getlist('extraction_type1', None)
        assignment_name1 = request.POST.getlist('assignment_name0', None)
        assignment_name2 = request.POST.getlist('assignment_name1', None)
        id=request.POST.getlist('wid',None)
        # print('receive_data:',request.POST)
        # print('api_name:',api_name,'next_api_name',next_api_name,'extraction_type1:',extraction_type1,'order_desc:',order_desc,'extraction_type2:',extraction_type2,'assignment_name1:',assignment_name1,'assignment_name2:',assignment_name2,id)
        # 定义循环次数
        frequency = int(len(order_desc))
        msg={'code':0,'message':"null",'date':time.strftime('%Y-%m-%d %H:%m:%S')}
        try:
            for i in range(frequency):
                if i>0:
                    print('try')
                    print(api_name[i], next_api_name[i], order_desc[i], extraction_type1[i], extraction_type2[i-1],
                          assignment_name1[i], assignment_name2[i-1], id[i])
                    models.Associated_api_modify(api_name=api_name[i], next_api_name=next_api_name[i],
                                                 order_desc=order_desc[i]
                                                 , extraction_type1=extraction_type1[i],
                                                 extraction_type2=extraction_type2[i - 1],
                                                 assignment_name1=assignment_name1[i],
                                                 assignment_name2=assignment_name2[i - 1], id=id[i])
                else:
                    print('two')
                    print(api_name[i], next_api_name[i], order_desc[i], extraction_type1[i],
                          assignment_name1[i], id[i])
                    models.Associated_api_modify(api_name=api_name[i], next_api_name=next_api_name[i],
                                                 order_desc=order_desc[i]
                                                 , extraction_type1=extraction_type1[i],
                                                 assignment_name1=assignment_name1[i],
                                                 id=id[i])
            msg['message']='success'
            return HttpResponse(json.dumps(msg))
        except Exception as e:
            msg['message']=e
            return HttpResponse(json.dumps(msg))


def Associated_api_delete(request):
    try:
        meg = {'code':0,'data':'ok'}
        id =request.GET.get('nid',None)
        print('ID:',id)
        models.Associated_api_delete(id)
        return HttpResponse(json.dumps(meg) )
    except Exception as e:
        meg = {'code': 1, 'data': e}
        return HttpResponse(json.dumps(meg))

def Associated_api_execute(request):
    pass

def Associated_api_execute_detail(request):
    pass