# @description: 连接mysql 数据库, 1、使用py
# @time: 20231106

import pymysql
import mysql.connector

def conn_pymysql(host,user,password,database):
    mydb = pymysql.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
    return mydb

def conn_mysql(host,user,password,database):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return mydb


if __name__=='__main__':
    host = "192.168.1.107"
    user = "root"
    password = "Findig-Dev-123"
    database = "zt"
    mydb = conn_pymysql(host,user,password,database)
    # mydb = conn_mysql(host,user,password,database)
    mycursor = mydb.cursor()
    # 执行 SQL 查询
    mycursor.execute("SELECT * FROM zt.COO_INDU_INFO")
    # 获取查询结果
    myresult = mycursor.fetchall()
    # 输出结果
    for x in myresult:
      print(x)