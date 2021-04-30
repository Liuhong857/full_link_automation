# -*- coding:utf-8 -*-
# author:liuhong

"""full_link_automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from cmdb import views


urlpatterns = [

    path('login/', views.login),
    path('main/', views.page),
    path('main/select/', views.select_data),
    # path('main/select/select/', views.select_data),
    # path('main/detail-(?P<nid>\d+)/', views.detail_data),
    path('main/detail/', views.detail_data),
    path('main/modify/', views.update_data),
    path('main/delete/', views.delete_data),
    path('main/execute/', views.execute_data),
    path('main/Associated_api/', views.Associated_api),
    path('main/Associated_api/detail/', views.Associated_api_detail),
    path('main/Associated_api/modify/', views.Associated_api_modify),
    path('main/Associated_api/delete/', views.Associated_api_delete),
    path('main/Associated_api/execute/', views.Associated_api_execute),
    path('main/Associated_api/execute_detail/', views.Associated_api_execute_detail),
    path('main/execute/detail', views.execute_detail),

]
