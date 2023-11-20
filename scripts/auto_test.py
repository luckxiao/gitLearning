
# ！env: python3.8
# @Author: HXl
# @Time: 2023.11.07
# @Descripts: 1、字段是否正确,与excel对比 2、注释是否正确,与excel对比
# 3、数据是否正确
# 4、映射是否正确


import oracledb
import pandas as pd
import mysql.connector

# 连接MySQL数据库
def conn_mysql(host,user,password,database):
    cnx = mysql.connector.connect(host=host,user=user,
                                  password=password,database=database)
    return cnx

# 连接Oracle数据库
def conn_oracle(lib_dir,dsn):
    # 添加 oracle 客户端路径
    oracledb.init_oracle_client(lib_dir=lib_dir)
    # orcale 连接信息
    conn_oracel = oracledb.Connection(dsn=dsn)
    return conn_oracel

if __name__ == '__main__':
    # mysql 连接信息
    host = "192.168.1.107"
    user = "root"
    password = "Findig-Dev-123"
    database = "wind_db"
    # oracle 连接信息
    lib_dir = "D:\\PLSQL\\product\\11.2.0\\dbhome_1\\bin"
    dsn = "bigdata_admin/qeGAB9Fx5DX32L9D3W5g@192.168.1.91:1521/bigdatadb"
    sql_query = """
    SELECT
            C.TABLE_SCHEMA,
            C.TABLE_NAME,
            T.TABLE_COMMENT,
            C.COLUMN_NAME,
            C.COLUMN_COMMENT,
            C.ORDINAL_POSITION,
            C.COLUMN_DEFAULT,
            C.IS_NULLABLE,
            C.DATA_TYPE,
            C.CHARACTER_MAXIMUM_LENGTH,
            C.CHARACTER_OCTET_LENGTH,
            C.NUMERIC_PRECISION,
            C.NUMERIC_SCALE
        FROM information_schema.TABLES T
        JOIN information_schema.COLUMNS C
            ON T.TABLE_NAME = C.TABLE_NAME AND T.TABLE_SCHEMA = C.TABLE_SCHEMA
        WHERE T.TABLE_SCHEMA  NOT IN ('sys','performance_schema','information_schema')
    		and t.TABLE_SCHEMA = 'test' and t.TABLE_NAME = 'fnd_insm_subj'
        ORDER BY C.TABLE_SCHEMA, C.TABLE_NAME, C.ORDINAL_POSITION
    """
    # 连接 mysql
    cnx = conn_mysql(user=user, password=password, host=host, database=database)
    mysql_cursor = cnx.cursor()
    mysql_cursor.execute(sql_query)
    table_info = mysql_cursor.fetchall()

    create_table_sql = ''
    table_columns = {}
    table_column_comment_infos = []
    table_comment_infos = {}
    # 获取表字段和注释
    for result in table_info:
        table_schema, table_name, table_comment, column_name, column_comment = result[0:5]
        # print(table_name.upper(),',',column_name,', --',column_comment.decode())
        table_column_comment_infos.append([column_name,column_comment.decode()])
    print(table_column_comment_infos)
    # 获取excel 中的字段和注释
    file_dir = 'D:\\table\\映射关系及监控设计.xlsx'
    dict_data = pd.read_excel(file_dir,sheet_name=[2])
    for i in range(len(dict_data[2]['表名'].values)):
        if(dict_data[2]['表名'].values[i] =='fnd_insm_subj'.upper()):
            print(dict_data[2]['表名'].values[i],',',dict_data[2]['字段名'].values[i],',','-- ',dict_data[2]['中文字段名'].values[i])




