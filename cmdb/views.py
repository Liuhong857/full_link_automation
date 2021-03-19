from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from  django.http import HttpResponse

# Create your views here.
from . import models

def add_data():#新增接口数据
    pass

def update_data():#修改数据
    pass
def delete_data():#删除数据
    pass
def select_data(request):#查询数据
    print('1',request.method)
    print('2',request.path_info)
    if request.method=='POST':

        api_name = request.POST.get('api_name', None)
        project = request.POST.get('project', None)
        create_user = request.POST.get('create_user', None)
        # api_name = request.GET.get('api_name', None)
        # project = request.GET.get('project', None)
        # create_user = request.GET.get('create_user', None)

        data = models.select_data(api_name,project,create_user)
        print(api_name,project,create_user)
        print('数据汇总:',data)


    # #
    # data = [{'id': 5, 'project': '1', 'api_name': '1', 'api_url': '1', 'api_data': '1', 'api_header': '1',
    #          'api_method': '1', 'api_response': None, 'create_time': '2021-03-18 14:33:53',
    #          'modify_time': '2021-03-18 14:33:53', 'modify_user_code': None}]
        return render(request, 'home_page.html', {'data': data},)
        # return render(request,'/page/main/select/',{'data': data})
    # else:
    #     return render(request, 'home_page.html',)


    else:
        print(1)
        return render(request, 'home_page.html',)


def page(request):
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
            # return render(request, 'test.html', {'data': data})
            pass
        else:
            pass

        # return render(request, 'home_page.html',locals())
                      # {'data': data})


    else:
        pass


