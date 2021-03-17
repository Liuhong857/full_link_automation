from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from  django.http import HttpResponse

# Create your views here.
import time

def add_data():#新增接口数据
    pass

def update_data():#修改数据
    pass
def delete_data():#删除数据
    pass
def select_data():#查询数据
    pass
def page(request):
    print(time.time())
    print(request.POST)
    return  render(request,'home_page.html')