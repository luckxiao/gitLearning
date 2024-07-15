#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024.06.21
# @Author  : huangxiaoli
# @descripts: 使用一个sheet 创建多张表的SQL语句
# @question:

import pandas as pd
import os
import re


# 将列表按照固定字符分割
def split_list(inpit_list,split_char):
    result = []   # 定义空列表,用于存放分割后的子列表
    sublist = []  # 定义空列表,存放当前的子列表
    for element in inpit_list: # 遍历带分隔的列表
        if element == split_char: # 判断当前的元素是否为分割字符
            result.append(sublist) # 如果是,将之前子列表添加到结果列表中,并创建一个新的子列表
            sublist =[]
        else:
            sublist.append(element) # 将不是分割字符添加到子列表中
    result.append(sublist)
    return result


if __name__ == '__main__':
    # database_name='WINDZX'
    # # database_name = 'FINCHINANEW'
    # #database_name = 'ZYYXZX'
    # source_name = 'WIND'
    database_name = 'jydb'
    source_name = 'JY'
    # 读取excel文件,sheet_name=None 表示引用所有的sheet
    #df = pd.read_excel("D:\\20230515\\wind映射表.xlsx",sheet_name=[0,1])
    # 文件夹名称
    file_name='D:\\最闻\\202407\\'
    dict_data = pd.read_excel(file_name + "股票基本信息&港股基本信息.xlsx", sheet_name=[3,],
                              skiprows=0)  # skiprows 跳过前第四行,sheet_name 索引从0开始，前闭后闭
    split_str = '    null                                      AS    nan, -- nan'
    for index,values in dict_data.items():
        query=[]
        table_name_set = set()
        file_name_set = set()
        for df_index,df_values in values.iterrows():
            table_name_china = str(df_values['表中文名'])
            target_table_name = str(df_values['表名'])
            source_table_name = str(df_values['来源表名'])
            columns = str(df_values['字段'])
            columns_desc = str(df_values['字段描述'])
            # 如果来源字段为空
            if str(df_values['来源字段']).strip() == 'nan':
                # print(str(df_values['来源字段']))
                source_columns = "null"
            else:
                source_columns = str(df_values['字段'])
            source_columns_name = str(df_values['来源字段名称'])
            if columns_desc != '记录编号' and columns_desc != '删除标识':
                if columns == 'F_TIME' or columns == 'U_TIME' or columns == 'G_TIME':
                    continue
                if source_columns == "null":
                    sql_comments = '    ' + source_columns.ljust(40) + '  AS    ' + columns+ ', -- ' + columns_desc
                    query.append(sql_comments)
                else:
                    sql_comments = '    ' + source_columns.ljust(40) + '  AS    ' + columns + ', -- ' + columns_desc
                    query.append(sql_comments)
            if columns_desc == '删除标识':
                if source_columns == "null":
                    sql_comments = '    ' + source_columns.ljust(40) + '  AS    ' + columns + ' -- ' + columns_desc
                    query.append(sql_comments)
                else:
                    sql_comments = '    ' + 'a.' + source_columns.ljust(40) + '  AS    ' + columns + ' -- ' + columns_desc
                    query.append(sql_comments)

            # 获取文件名称和来源表名
            if source_table_name != 'nan' and target_table_name != 'nan':
                file_name_set.add(source_table_name+'-'+target_table_name)
                table_name_set.add(source_table_name)
        print(query)
        result_list = split_list(query,split_str)
        file_name_list = list(file_name_set) # 文件名称
        source_table_name_list = list(table_name_set)  # 来源表名称
        # 来源表名称 + 中间的SQL语句 生成字典
        result_dict = dict(zip(source_table_name_list,result_list))
        # print(result_dict)
        # 切换到目标文件夹所在的位置
        os.chdir(file_name)
        # 创建子文件夹的名称
        folder_name = '测试\\sql'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # 循环文件名称
        for file_name_one in file_name_list:
            output_file = f"{file_name}{folder_name}\\{source_name}_{file_name_one}.sql".format(file_name=file_name,folder_name=folder_name,source_name=source_name,file_name_one=file_name_one)
            # print(output_file)
            with open(output_file,'w',encoding='utf-8') as f1:
                # 遍历字典生成sql语句
                for source_table_name, columns_data in result_dict.items():
                    sql_columns = '\n'.join([str(columns_data_slipt) for columns_data_slipt in columns_data])
                    all_sql_columns = 'select' + '\n' + sql_columns + '\n' + 'from ' + database_name + '.' + source_table_name+' a'
                    # 字符串开头包含来源表名
                    if file_name_one.startswith(source_table_name):
                        # print(all_sql_columns)
                        f1.write(all_sql_columns)
            f1.close()
