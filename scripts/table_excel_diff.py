
# ！env: python3.8
# @Author: HXl
# @Time: 2023.11.07
# @Descripts: 1、字段、注释是否正确,与excel对比;


import oracledb
import pandas as pd
import mysql.connector
import sqlConnect

def Table_Excel_DIFF():
    # 连接 mysql
    table_info = sqlConnect.conn_mysql_target(host, user, password, database, sql_query)

    table_name_keys = ['FND_MNGR', 'FND_ISS']
    table_column_comment_infos = {}
    table_column_comment_infos_excel = {}

    # 获取表字段和注释
    for result in table_info:
        table_schema, table_name, table_comment, column_name, column_comment = result[0:5]
        column_comment = '{column_name} -- {column_comment}'.format(column_name=column_name.upper(),
                                                                    column_comment=column_comment.decode())
        # 将数据按照表为key的方式组成字段
        table_column_comment_infos.setdefault(table_name.upper(), []).append(column_comment)
    # print(table_column_comment_infos)

    # 获取excel 中的字段和注释
    file_dir = 'D:\\table\\映射关系及监控设计.xlsx'
    dict_data = pd.read_excel(file_dir, sheet_name=[2])
    for i in range(len(dict_data[2]['表名'])):
        for tabel_name_key in table_name_keys:
            if dict_data[2]['是否进入模型'].values[i] == 1 and dict_data[2]['表名'].values[i] == tabel_name_key:
                column_comment_excel = '{column_name_excel} -- {column_comment_excel}'.format(
                    column_name_excel=dict_data[2]['字段名'].values[i],
                    column_comment_excel=dict_data[2]['中文字段名'].values[i])
                table_column_comment_infos_excel.setdefault(dict_data[2]['表名'].values[i], []).append(
                    column_comment_excel)
    # print(table_column_comment_infos_excel)

    # 通过列表推导式比较表字段和excel字段的差异
    for key, values in table_column_comment_infos.items():
        for key_excel, values_excel in table_column_comment_infos_excel.items():
            if (key == key_excel):
                list_common = [item for item in values if item in values_excel]
                # 将excel与表进行对比, 表中存在但是excel中不存在
                list_different = [item_diff for item_diff in values if item_diff not in list_common]
                output_foramt = '{key} 表中存在但是 excel 中不存在: {list_different}'.format(key=key,
                                                                                             list_different=list_different)
                print(output_foramt)
                list_different_excel = [item_diff_excel for item_diff_excel in values_excel if
                                        item_diff_excel not in list_common]
                output_foramt_excel = '{key} 表中不存在但是 excel 中存在: {list_different_excel}'.format(key=key,
                                                                                                         list_different_excel=list_different_excel)
                print(output_foramt_excel)


if __name__ == '__main__':
    # mysql 连接信息
    host = "192.168.1.107"
    user = "root"
    password = "Findig-Dev-123"
    database = "wind_db"
    # oracle 连接信息
    # lib_dir = "D:\\PLSQL\\product\\11.2.0\\dbhome_1\\bin"
    # dsn = "bigdata_admin/qeGAB9Fx5DX32L9D3W5g@192.168.1.91:1521/bigdatadb"
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
    		and t.TABLE_SCHEMA = 'test' and t.TABLE_NAME in('FND_MNGR','FND_ISS')
        ORDER BY C.TABLE_SCHEMA, C.TABLE_NAME, C.ORDINAL_POSITION 
    """
    Table_Excel_DIFF()


