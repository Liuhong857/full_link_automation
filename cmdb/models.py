from django.db import models

# Create your models here.
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='test')
cursor = db.cursor()

def add_data(project,api_name,api_url,api_data,api_header,api_method):
    sql = '''insert INTO t_api_data (project,api_name,api_url,api_data,api_header,api_method,create_time,modify_time) VALUES('%s','%s','%s','%s','%s','%s',NOW(),NOW())'''%(project,api_name,api_url,api_data,api_header,api_method)
    print(sql)
    cursor.execute(sql)
    db.commit()

def select_data(api_name=None,project=None,create_user=None):

    if api_name=='' and project=='' and create_user=='':
        print('查询全表')

        sql='''select * from t_api_data ;'''
        print(sql)
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        print(data_dict)
        return data_dict
    else:
        sql ='''select * from t_api_data where api_name='%s'  or project ='%s' or modify_user_code='%s'; '''%(api_name,project,create_user)
        print(sql)
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]# 列表表达式把数据组装起来
        print(data_dict)
        return data_dict