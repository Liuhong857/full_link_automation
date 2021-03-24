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
        # print('查询全表')

        sql='''select id,project,api_name,api_url,api_data,api_header,api_method,api_response,api_code,CAST(create_time AS CHAR) AS create_time,CAST(modify_time AS CHAR) AS modify_time,modify_user_code from t_api_data ;'''
        # print(sql)
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        # print('da;',data_dict)
        return data_dict
    elif api_name==None and project==None and create_user==None:
        # print('None全表')

        sql='''select id,project,api_name,api_url,api_data,api_header,api_method,api_response,CAST(create_time AS CHAR) AS create_time,CAST(modify_time AS CHAR) AS modify_time,modify_user_code from t_api_data ;'''
        # print(sql)
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        # print('da;',data_dict)
        return data_dict
    else:
        sql ='''select id,project,api_name,api_url,api_data,api_header,api_method,api_response,CAST(create_time AS CHAR) AS create_time,CAST(modify_time AS CHAR) AS modify_time,modify_user_code from t_api_data where api_name='%s'  or project ='%s' or modify_user_code='%s'; '''%(api_name,project,create_user)
        # print(sql)
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]# 列表表达式把数据组装起来
        # print(data_dict)
        return data_dict

def select_detail(id):
    sql = '''select id,project,api_name,api_url,api_data,api_header,api_method,api_response,CAST(create_time AS CHAR) AS create_time,CAST(modify_time AS CHAR) AS modify_time,modify_user_code from t_api_data where id='%s';'''%(id)
    cursor.execute(sql)
    desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
    return data_dict

def update_data(id,api_url,api_header,api_method,api_name,api_data):
    sql ='''UPDATE t_api_data SET  api_name='%s' ,  api_url='%s', api_header='%s' , api_method='%s' , api_data='%s' where id='%s';'''%(api_name,api_url,api_header,api_method,api_data,id)
    print(sql)
    cursor.execute(sql)
    db.commit()
    update_data_list = select_detail(id)
    return update_data_list

def delete_data(id):
    sql= '''delete from t_api_data where id='%s';'''%id
    print(sql)
    cursor.execute(sql)
    db.commit()
    data=select_detail(id)
    return data

def update_api_data(id,response,code):
    sql='''UPDATE t_api_data SET  api_response="%s",api_code="%s" where id='%s';'''%(response,code,id)
    print(sql)
    cursor.execute(sql)
    db.commit()
    update_execute_data(id)

def update_execute_data(id):#更新执行记录
    sql ='''insert INTO t_api_execute_detail (project,api_name,api_url,api_data,api_header,api_method,api_response,api_code,api_id,create_time)SELECT project,api_name,api_url,api_data,api_header,api_method,api_response,api_code,id,NOW() from t_api_data where id='%s';'''%(id)
    print(sql)
    cursor.execute(sql)
    db.commit()