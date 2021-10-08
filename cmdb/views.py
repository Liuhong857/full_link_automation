# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from cmdb import models
from  django.http import HttpResponse

from .encapsulation_request import *
# from cmdb.encapsulation_request import *

# Create your views here.
from . import models
import json
import jmespath
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

    return redirect('/page/main/select/?p=1')

def select_data(request):#查询数据

    if request.method=='POST':
        api_name = request.POST.get('api_name', None)
        project = request.POST.get('project', None)
        create_user = request.POST.get('create_user', None)
        data = models.select_data(api_name,project,create_user)
        print(api_name,project,create_user)
        # print('数据汇总:',data)


        count_data,y=divmod(len(data),10)
        if y:
            count_data +=1
        page_list= []
        for i in range(1,count_data+1):
            if i==1:
                temp = '<a style" style="text-decoration: none;color: orange;display: inline-block;padding: 5px;background-color: #777777;margin: 5px;background-color: brown;color: white;" href="/page/main/select/?p=%s">%s</a>'%(i,i)
                page_list.append(temp)
            else:
                temp = '<a style" style="text-decoration: none;color: orange;display: inline-block;padding: 5px;background-color: #777777;margin: 5px" href="/page/main/select/?p=%s">%s</a>'%(i,i)
                page_list.append(temp)

        page_list="".join(page_list)
        if len(data)>10:
            data=data[0:10]


        return render(request, 'home_page.html', {'data': data,'page_list':page_list},)
    elif  request.method=='GET':
        api_name = request.GET.get('api_name', None)
        project = request.GET.get('project', None)
        create_user = request.GET.get('create_user', None)
        p = request.GET.get('p', None)
        data = models.select_data(api_name,project,create_user)
        count_data, y = divmod(len(data), 10)
        if y:
            count_data += 1
        page_list = []
        for i in range(1, count_data + 1):
            if i== int(p):
                temp = '<a style" style="text-decoration: none;color: orange;display: inline-block;padding: 5px;background-color: #777777;margin: 5px;background-color: brown;color: white;" href="/page/main/select/?p=%s">%s</a>'%(i,i)
                page_list.append(temp)
            else:
                temp = '<a style="text-decoration: none;color: orange;display: inline-block;padding: 5px;background-color: #777777;margin: 5px" href="/page/main/select/?p=%s">%s</a>' % (
                i, i)
                page_list.append(temp)

        page_list = "".join(page_list)
        print('page_list',page_list)
        if p!=None:
            p = int(p)
            data = data[(p-1)*10:p*10]

        return render(request, 'home_page.html', {'data': data,'page_list':page_list},)


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
    database_result = models.select_detail(id=id)
    # print(type(database_result[0]))
    api_url = database_result[0]['api_url']
    api_data = database_result[0]['api_data']
    api_header = database_result[0]['api_header']
    api_method = database_result[0]['api_method']
    print('api_header',api_header)
    headers = json.loads(api_header)#该requestsAPI明确规定，headers必须是一个字典：

    result = RunMain(url=api_url,data=api_data,method=api_method,headers=headers)
    response = result.result
    print(response)

    if response.get('result',None) != None:
        if response.get('result',None).get('lastmileLabel',None)!= None:
            response['result']['lastmileLabel']=''
    if response.get('hasBusinessException',None)!=None:
        response['hasBusinessException']= ''
    if response.get('success', None) != None:
        response['success']= ''

    new_response=str(response).replace("'", '"')

    code = result.code
    print(new_response)
    print(code)
    # response= json.dumps(response)
    models.update_api_data(id,new_response,code)
    return redirect('/page/main/select/?p=1')

def Associated_api(request):#API关联关系

    # print(request.method)
    if request.method=='GET':
        data = models.select_data()
        return render(request,'Associated_api1.html',{'data': data},)
    elif request.method=='POST':
        print(request.POST.get('name',None))
        values= request.POST.get('name',None)

        if values=='select':
            data = models.select_data()
            select = models.select_Associated_api()
            print('开始调试...')
            return  render(request,'Associated_api1.html',{'select': select,'data': data},)
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
                    print('try ')
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


def update_dict(k, v, mydict):
    print(type(mydict),mydict)

    if isinstance(mydict, dict):
        for element_key in mydict.keys():
            if element_key == k:
                print('赋值')
                mydict[element_key] = v
            elif isinstance(mydict[element_key], dict):
                for element_key1 in mydict[element_key].keys():
                    if element_key1 == k:
                        print('赋值')
                        mydict[element_key][element_key1] = v
                    elif isinstance(mydict[element_key][element_key1], dict):
                        for element_key2 in mydict[element_key][element_key1].keys():
                            if element_key2 == k:
                                print('赋值')
                                mydict[element_key][element_key1][element_key2] = v
                            elif isinstance(mydict[element_key][element_key1][element_key2], dict):
                                for element_key3 in mydict[element_key][element_key1][element_key2].keys():
                                    if element_key3 == k:
                                        print('赋值')
                                        mydict[element_key][element_key1][element_key2][element_key3] = v
                            elif isinstance(mydict[element_key][element_key1][element_key2], list):
                                pass

                    elif isinstance(mydict[element_key][element_key1], list):
                        for element_dict_list in mydict[element_key][element_key1]:
                            if isinstance(element_dict_list, dict):
                                for element_dict_list_1 in element_dict_list.keys():
                                    if element_dict_list_1 == k:
                                        print('dictlist赋值')
                                        element_dict_list[element_dict_list_1] = v
                                    elif isinstance(element_dict_list_1, dict):
                                        pass
                                    elif isinstance(element_dict_list_1, list):
                                        for element_dict_list_1_list in element_dict_list_1:
                                            if isinstance(element_dict_list_1_list, dict):
                                                for element_dict_list_1_list_dict in element_dict_list_1_list.keys():
                                                    if element_dict_list_1_list_dict == k:
                                                        print('dictlist赋值')
                                                        element_dict_list_1[element_dict_list_1_list][
                                                            element_dict_list_1_list_dict] = v


                            elif isinstance(element_dict_list, list):
                                for element_dict_list_2 in element_dict_list:
                                    if isinstance(element_dict_list_2, dict):
                                        for element_dict_list3 in element_dict_list_2:
                                            if element_dict_list3 == k:
                                                print('dictlist赋值')
                                                element_dict_list_2[element_dict_list3] = v

                                    elif isinstance(element_dict_list_2, list):
                                        pass

            elif isinstance(mydict[element_key], list):
                for element_dict_list_list in mydict[element_key]:
                    if isinstance(element_dict_list_list, dict):
                        for element_dict_list_list_dict in element_dict_list_list.keys():
                            if element_dict_list_list_dict == k:
                                print('赋值')
                                element_dict_list_list[element_dict_list_list_dict] = v
                            elif isinstance(element_dict_list_list_dict, dict):
                                for element_dict_list_list_dict_dict in element_dict_list_list_dict.keys():
                                    if element_dict_list_list_dict_dict == k:
                                        element_key[element_dict_list_list][element_dict_list_list_dict] = v
                                    elif isinstance(element_dict_list_list_dict_dict, dict):
                                        for element_dict_list_list_dict_dict_dict in element_dict_list_list_dict_dict.keys():
                                            if element_dict_list_list_dict_dict_dict == k:
                                                print('赋值')
                                                element_key[element_dict_list_list][element_dict_list_list_dict][
                                                    element_dict_list_list_dict_dict_dict] = v

                            elif isinstance(element_dict_list_list_dict, list):
                                for element_dict_list_list_dict_list in element_dict_list_list_dict:
                                    if isinstance(element_dict_list_list_dict_list, dict):
                                        for element_dict_list_list_dict_list_dict in element_dict_list_list_dict_list.keys():
                                            if element_dict_list_list_dict_list_dict == k:
                                                print('赋值')
                                                element_dict_list_list_dict[element_dict_list_list_dict_list][
                                                    element_dict_list_list_dict_list_dict] = v
                                            elif isinstance(element_dict_list_list_dict_list_dict, dict):
                                                for element_dict_list_list_dict_list_dict_dict in element_dict_list_list_dict_list_dict.keys():
                                                    if element_dict_list_list_dict_list_dict_dict == k:
                                                        print('赋值')
                                                        element_dict_list_list_dict[element_dict_list_list_dict_list][
                                                            element_dict_list_list_dict_list_dict][
                                                            element_dict_list_list_dict_list_dict] = v




                                            elif isinstance(element_dict_list_list_dict_list_dict, list):
                                                for element_dict_list_list_dict_list_dict_list in element_dict_list_list_dict_list_dict:
                                                    if isinstance(element_dict_list_list_dict_list_dict_list, dict):
                                                        for element_dict_list_list_dict_list_dict_list_dict in element_dict_list_list_dict_list_dict_list.keys():
                                                            if element_dict_list_list_dict_list_dict_list_dict == k:
                                                                print('赋值')
                                                                element_dict_list_list_dict_list_dict[
                                                                    element_dict_list_list_dict_list_dict_list][
                                                                    element_dict_list_list_dict_list_dict_list_dict] = v

                                                            elif isinstance(
                                                                    element_dict_list_list_dict_list_dict_list_dict,
                                                                    dict):
                                                                for element_dict_list_list_dict_list_dict_list_dict_dict in element_dict_list_list_dict_list_dict_list_dict.keys():
                                                                    if element_dict_list_list_dict_list_dict_list_dict_dict == k:
                                                                        element_dict_list_list_dict_list_dict[
                                                                            element_dict_list_list_dict_list_dict_list][
                                                                            element_dict_list_list_dict_list_dict_list_dict][
                                                                            element_dict_list_list_dict_list_dict_list_dict] = v




    elif isinstance(mydict, list):
        for element_list in mydict:
            if isinstance(element_list, dict):
                for element_list_1 in element_list.keys():
                    if element_list_1 == k:
                        print('list赋值')
                        element_list[element_list_1] = v
                    elif isinstance(element_list_1, dict):
                        for element_list_dict in element_list_1.keys():
                            if element_list_dict == k:
                                print('list赋值')
                                element_list[element_list_1][element_list_dict] = v
                            elif isinstance(element_list[element_list_1][element_list_dict], dict):
                                for element_list_dict_dict in element_list[element_list_1][element_list_dict].keys():
                                    if element_list_dict_dict == k:
                                        print("list赋值")
                                        element_list[element_list_1][element_list_dict][element_list_dict_dict] = v
                    elif isinstance(element_list_1, list):
                        for element_list_list in element_list_1:
                            if isinstance(element_list_list, dict):
                                for element_list_list_dict in element_list_list.keys():
                                    if element_list_list_dict == k:
                                        print("list赋值")
                                        element_list_list[element_list_list_dict] = v
                                    elif isinstance(element_list_list_dict, dict):
                                        for element_list_list_dict_dict in element_list_list_dict.keys():
                                            if element_list_list_dict_dict == k:
                                                element_list_list[element_list_list_dict][
                                                    element_list_list_dict_dict] = v


                            elif isinstance(element_list_list, list):
                                pass




            elif isinstance(element_list, list):
                pass

    return mydict

def Associated_execute_data(database_result,api_data=None):#执行API循环请求
    count =0
    id = database_result[0]['id']
    api_url = database_result[0]['api_url']
    if api_data==None:
        api_data = database_result[0]['api_data']
        count+=1
    api_header = database_result[0]['api_header']
    api_method = database_result[0]['api_method']
    headers = json.loads(api_header)#该requestsAPI明确规定，headers必须是一个字典：
    print('api_data:',api_data)
    api_data = str(api_data).replace("'", '"').replace("False","false")
    print('api_url:',api_url,'api_header:',api_header,'api_method:',api_method,'api_data:',api_data)

    result = RunMain(url=api_url,data=api_data,method=api_method,headers=headers)
    response = result.result
    #注释掉换单的label数据
    if response.get('result',None)!=None:
        if response.get('result', None).get('lastmileLabel', None)!=None:
            response['result']['lastmileLabel']=''
    elif response.get('data',None)!=None:
        if response.get('data',None).get('bagLabelList',None)!=None:
            response.get('data', None).get('bagLabelList', None)[0]['bagLabel']=''
    if response.get('success',None)!=None:
        response['success']=''

    code = result.code

    new_response=str(response).replace("'", '"')
    print(new_response)
    print(code)
    print('api_data:',api_data)

    if count==0:
        models.update_api_data(id=id,response=new_response,code=code,api_data=api_data)
    else:
        models.update_api_data(id=id,response=new_response,code=code)
    time.sleep(10)
    return response
def Associated_api_execute(request):

    id=request.GET.get('nid',None)
    data =models.Associated_api_ready_0(id)
    #定义循环顺序
    print(data)
    sequence = int(len(data))
    print(sequence)

    for i  in range(sequence):
        print('i:',i)

        if i ==0:
            api_name = data[i]['api_name']
            first_request=models.Associated_api_execute_select(name=api_name)
            # print(first_request)
            #保存第一个请求返回结果
            first_response=Associated_execute_data(first_request)
            print(first_response)

            next_api_name = data[i]['next_api_name']
            next_request = models.Associated_api_execute_select(name=next_api_name)
            # next_api_request =json.loads(next_request[0]['api_data'])
            next_api_request =eval(next_request[0]['api_data'])

            print('next_api_request:',type(next_api_request),next_api_request)


            extraction_type_0 = data[i]['extraction_type_0']
            assignment_name0 = data[i]['assignment_name0']

            if extraction_type_0.count('@')==0:

                #请求格式切片赋值
                extraction_type = extraction_type_0.split('|')
                print('extraction_type',extraction_type)
            else:
                extraction_type = extraction_type_0.split('@')
                extraction_type_obtain = extraction_type[0]
                extraction_type_obtain=models.Associated_api_execute_select(extraction_type_obtain)
                first_response = extraction_type_obtain[0]['api_response']
                extraction_type =extraction_type[1].split('|')


            #赋值格式进行切片
            assignment_name = assignment_name0.split('|')
            print('assignment_name',assignment_name)
            if len(assignment_name)!=0 or len(extraction_type)!=0:
                for row in range(int(len(extraction_type))):
                    assignment_value= jmespath.search(extraction_type[row],first_response)
                    print(assignment_value)
                    assignment_key = assignment_name[row].split('.')[-1]
                    updata_next_api_request=update_dict(assignment_key,assignment_value,next_api_request)

            print(updata_next_api_request)
            # 保存next结果
            next_response=Associated_execute_data(next_request,updata_next_api_request)
            print(next_response)


        else:
            #获取上一个的请求的name
            previous_name = data[i-1]['next_api_name']
            api_name = data[i]['api_name']
            next_api_name = data[i]['next_api_name']
            extraction_type_0 = data[i]['extraction_type_0']
            assignment_name0 = data[i]['assignment_name0']
            extraction_type_1 = data[i]['extraction_type_1']
            assignment_name1 = data[i]['assignment_name1']
            #上个请求数据
            previous_name_response_data = models.Associated_api_execute_select(name=previous_name)
            #本次请求的数据
            first_request = models.Associated_api_execute_select(name=api_name)
            #下一个接口请求的数据
            next_request = models.Associated_api_execute_select(name=next_api_name)

            if len(extraction_type_0)==0 or len(assignment_name0)==0  :
                first_response = Associated_execute_data(first_request)
                if len(extraction_type_1)==0 or len(assignment_name1)==0:
                    next_response = Associated_execute_data(next_request)

            else:
                if extraction_type_0.count('@')==0:
                    extraction_type_0= extraction_type_0.split('|')
                    for i1 in range(int(len(extraction_type_0))):
                        try:
                            data_i1=extraction_type_0[i1]
                            previous_name_response=eval(previous_name_response_data[0]['api_response'])

                            print('previous_name_response:',previous_name_response,type(previous_name_response))
                            one_vlues= jmespath.search(data_i1,previous_name_response)
                            one_key=assignment_name0.split('|')[i1].split('.')[-1]
                            print('first_request:',first_request[0]['api_data'])
                            first_request_api_data_change = eval(first_request[0]['api_data'])

                            print('first_request_api_data_change:', first_request_api_data_change,
                                  type(first_request_api_data_change))
                        except Exception as e:
                            print('e:',e)

                        first_request_api_data_update = update_dict(one_key, one_vlues,
                                                                    first_request_api_data_change)
                        first_ask_response = Associated_execute_data(first_request, json.dumps(first_request_api_data_update))
                        print('first_ask_response:', first_ask_response)

                        #第一次请求


                        if extraction_type_1.count('@')==0:
                            extraction_type_1= extraction_type_1.split('|')
                            for i2 in range(int(len(extraction_type_1))):
                                try:
                                    data_i2 = extraction_type_1[i2]
                                    two_vlues = jmespath.search(data_i1, first_ask_response)
                                    two_key = assignment_name1.split('|')[i2].split('.')[-1]
                                    next_request_api_data = eval(next_request[0]['api_data'])


                                except Exception as e:
                                    print(e)
                                two_request_api_data=update_dict(two_key,two_vlues,next_request_api_data)
                                two_ask_response = Associated_execute_data(next_request, json.dumps(two_request_api_data))
                                print('two_ask_response:',two_ask_response)
                        else:
                            try:
                                name_obtain_next = extraction_type_1.split('@')[0]
                                extraction_type_1=extraction_type_1.split('@')[1].split('|')
                                print('extraction_type_1:',extraction_type_1)
                                # 指定获取response
                                appoint_next_response = models.Associated_api_execute_select(name=name_obtain_next)
                                appoint_next_response_data = eval(appoint_next_response[0]['api_response'])
                                print(next_request)
                                next_request_api_data = eval(next_request[0]['api_data'])
                                print('four_next_requs_data:',next_request_api_data,type(next_request_api_data))


                                for appoint_next_row in range(int(len(extraction_type_1))):
                                    appoint_next_value = extraction_type_1[appoint_next_row]
                                    appoint_next_value = jmespath.search(appoint_next_value,appoint_next_response_data)
                                    four_key = assignment_name1.split('|')[appoint_next_row].split('.')[-1]
                                    four_request_api_data = update_dict(four_key, appoint_next_value, next_request_api_data)
                                    four_ask_response = Associated_execute_data(next_request, four_request_api_data)
                                    print('four_ask_response:', four_ask_response)


                            except Exception as e:
                                print('e:9',e)
                else:
                    try:
                        name_obtain=extraction_type_0.split('@')[0]
                        extraction_type_0=extraction_type_0.split('@')[1].split('|')
                        #指定获取response
                        appoint_response = models.Associated_api_execute_select(name=name_obtain)
                        appoint_response_data=eval(appoint_response[0]['api_response'])
                        first_request_api_data = eval(first_request[0]['api_data'])

                        for appoint_row in range(int(len(extraction_type_0))):
                            appoint_value = extraction_type_0[appoint_row]
                            appoint_value= jmespath.search(appoint_value,appoint_response_data)
                            three_key = assignment_name0.split('|')[appoint_row].split('.')[-1]
                            three_request_api_data = update_dict(three_key, appoint_value, first_request_api_data)
                            three_ask_response = Associated_execute_data(first_request, json.dumps(three_request_api_data))
                            print('three_ask_response:', three_ask_response)

                    except Exception as e:
                        print(e)

    return HttpResponse('ok')




def Associated_api_execute_detail(request):
    id = request.GET.get('nid')
    api_name_data =models.Associated_execute_result_first(id)
    next_api_name_data = models.Associated_execute_result_next(id)

    return render(request,'Associated_api_execute_detail.html',{'data':api_name_data,'next_data':next_api_name_data},)

def execute_detail(request):
    id = request.GET.get('nid')
    executed_detail =models.api_execute_detail(id)

    return render(request,'api_data_execute_record.html',{'executed_detail':executed_detail},)

