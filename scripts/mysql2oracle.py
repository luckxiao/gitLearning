
# -*- encoding: utf-8 -*-
"""
@File:        mysql2oracle.py
@Author:      Huangxiaoli
@Time:        2023/11/07
@description:    将 mysql 表结构转换成 oracle 表结构
"""

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

# mysql 连接信息
host = "192.168.1.107"
user = "root"
password = "Findig-Dev-123"
database = "wind_db"
# oracle 连接信息
lib_dir = "D:\\PLSQL\\product\\11.2.0\\dbhome_1\\bin"
dsn = "bigdata_admin/qeGAB9Fx5DX32L9D3W5g@192.168.1.91:1521/bigdatadb"

mysql_to_oracle_map = {
    'int': 'NUMBER',
    'bigint': 'NUMBER',
    'float': 'NUMBER',
    'double': 'NUMBER',
    'decimal': 'NUMBER',
    'varchar': 'VARCHAR2',
    'longtext': 'VARCHAR2',
    'mediumtext': 'VARCHAR2',
    'char': 'CHAR',
    'text': 'VARCHAR2',
    'blob': 'BLOB',
    'datetime': 'DATE',
    'timestamp': 'DATE',
    'date': 'DATE'
}
sql_query = """SELECT
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
        ORDER BY C.TABLE_SCHEMA, C.TABLE_NAME, C.ORDINAL_POSITION"""
# 连接 mysql
cnx = conn_mysql(user=user, password=password,host=host, database=database)
mysql_cursor = cnx.cursor()
# 获取MySQL表结构信息
mysql_cursor.execute(sql_query)
table_info = mysql_cursor.fetchall()

create_table_sql = ''
table_columns = {}
table_column_comment_infos = []
table_comment_infos = {}
for result in table_info:
    table_schema, table_name, table_comment, column_name, column_comment, ordinal_position, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_scale = result
    table_comment_infos[table_name] = table_comment
    table_column_comment_infos.append([table_name, column_name, column_comment])
    if table_name not in table_columns:
        table_columns[table_name] = []

    column_sql = '\t{} {}'.format(column_name, mysql_to_oracle_map[data_type.decode()])

    if character_octet_length:
        character_octet_length = 4000 if character_octet_length >= 4000 else character_octet_length
        column_sql += '({})'.format(character_octet_length)
    elif numeric_precision:
        column_sql += '({},{})'.format(numeric_precision, numeric_scale)
    if is_nullable == 'NO':
        column_sql += ' NOT NULL'
    table_columns[table_name].append(column_sql)

    # if column_default is not None:
    #     column_sql += ' DEFAULT {}'.format(column_default)

for key, columns in table_columns.items():
    create_table_sql += 'CREATE TABLE {} (\n'.format(key)
    create_table_sql += ',\n'.join(columns)
    create_table_sql += '\n);\n\n'

    table_comment = table_comment_infos[key]
    if table_comment:
        create_table_sql += "COMMENT ON TABLE {} IS '{}';\n\n".format(key, table_comment)

    for table_name, column_name, column_comment in table_column_comment_infos:
        if table_name == key and column_comment:
            create_table_sql += "COMMENT ON COLUMN {}.{} IS '{}';\n".format(table_name, column_name, column_comment.decode())
# print(create_table_sql.upper())

# 文件输出路径
output_file = "D:\\table\\{table_name}.sql".format(table_name=table_name)
# 追加写入文件
with open(output_file, 'w') as f1:
    f1.write("{create_table_sql}"
             .format(create_table_sql=create_table_sql.upper()))
f1.close()

