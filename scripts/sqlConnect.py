# ！env: python3.8
# @Author:hxl
# @Time:20231127
# @Descripts: 数据库连接

import oracledb
import mysql.connector

# 连接MySQL数据库
def conn_mysql_target(host,user,password,database,target_sql_query):
    cnx = mysql.connector.connect(host=host, user=user,
                                  password=password, database=database)
    mysql_cursor = cnx.cursor()
    mysql_cursor.execute(target_sql_query)
    table_info = mysql_cursor.fetchall()
    return table_info

# 连接MySQL数据库
def conn_mysql_source(host,user,password,database,source_sql_query):
    cnx = mysql.connector.connect(host=host, user=user,
                                  password=password, database=database)
    mysql_cursor = cnx.cursor()
    mysql_cursor.execute(source_sql_query)
    table_info = mysql_cursor.fetchall()
    return table_info

# 连接Oracle数据库
def conn_oracle(lib_dir, dsn):
    # 添加 oracle 客户端路径
    oracledb.init_oracle_client(lib_dir=lib_dir)
    # orcale 连接信息
    conn_oracel = oracledb.Connection(dsn=dsn)
    return conn_oracel


