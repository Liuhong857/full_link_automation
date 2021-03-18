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
def select_data():#查询数据
    pass
def page(request):
    print(request.POST)
    print(request.POST.get('operation_name', None))
    if request.method=='POST':
        data=''

        if request.POST.get('operation_name', None) == 'add':
            project = request.POST.get('project', None)
            project_name = request.POST.get('project_name', None)
            url = request.POST.get('url', None)
            data = request.POST.get('data', None)
            header = request.POST.get('header', None)
            method = request.POST.get('method', None)
            models.add_data(project,project_name,url,data,header,method)
        elif request.POST.get('operation_name', None) == 'select':
            api_name = request.POST.get('api_name', None)
            project = request.POST.get('project', None)
            create_user = request.POST.get('create_user', None)
            data = models.select_data(api_name,project,create_user)
            data=data
            print(type(data),data)
            # msg = {'msg': data}
            # print(msg,type(msg))
            # print(msg['msg'][0])

        else:
            pass

        return render(request, 'home_page.html', {'data': data})
    else:
        return render(request, 'home_page.html')



