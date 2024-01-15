# @descripts:将excel转换成SQL查询的格式
# @time:2023.10.23
# @question:需要封装

import pandas as pd
import os

# 拼接 SQL 中间的 格式
def read_m_data(query,columns_source,columns_targe,columns_comment,flag):
    if flag==0:
        query.append("    {columns_source} as {columns_targe}, -- {columns_comment}" \
                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                             columns_comment=columns_comment))
    if flag==1:
        query.append("    {columns_source} as {columns_targe} -- {columns_comment}" \
                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                             columns_comment=columns_comment))

if __name__ == '__main__':
    database_name='WINDZX'
    # database_name = 'FINCHINANEW'
    #database_name = 'ZYYXZX'
    source_name = 'WIND'
    # 读取excel文件,sheet_name=None 表示引用所有的sheet
    #df = pd.read_excel("D:\\20230515\\wind映射表.xlsx",sheet_name=[0,1])
    # 文件夹名称
    file_name='D:\\2024.01\\'
    dict_data = pd.read_excel(file_name + "新增_stt.xlsx", sheet_name=[1,2,3,4,5,6],
                              skiprows=4)  # skiprows 跳过前第四行,sheet_name 索引从0开始，前闭后闭
    # sheet 的数据量
    for sheet_num in list(dict_data.keys()):
        # 获取目标表名称
        target_table_name = dict_data[sheet_num]['目标表名称'][1]
        source_table_name = dict_data[sheet_num]['来源表名'][2]
        sheet_len = len(dict_data[sheet_num])  # sheet 长度
        query = []
        for index, row in dict_data[sheet_num].iterrows():
            columns_source = row[9]  # 源字段
            if (str(columns_source).lower() == 'nan'):  # 如果源为空则给null；excel空白处，默认是float类型，需转换为str
                columns_source = "null"
            columns_targe = row[5]  # 目标字段
            columns_comment = row[6]  # 目标注释
            if (index == sheet_len - 1):  # 如果为最后一行，则不加逗号
                columns_source = '\'' + str(source_table_name).upper() + '\'' + '||OBJECT_ID'  # object_id 为业务主键
                columns_targe = 'INC_ID_S'
                read_m_data(query,columns_source,columns_targe,columns_comment,1)
            else:
                if (str(columns_targe).upper() == 'REC_IN_TAB_TIME' or str(
                        columns_targe).upper() == 'REC_UPT_TIME' or str(columns_targe).upper() == 'REC_ACHV_TIME'):
                    continue
                else:
                    if str(columns_targe).upper() == 'SRC_ID':
                        columns_source = '\'' + f'{source_name}.'.format(source_name=source_name) + str(source_table_name).upper() + '\''
                        read_m_data(query,columns_source, columns_targe, columns_comment, 0)
                    elif str(columns_targe).upper() == 'DEL_FLAG':
                        columns_source = '\'' + '0' + '\''
                        read_m_data(query,columns_source, columns_targe, columns_comment, 0)
                    else:
                        read_m_data(query,columns_source, columns_targe, columns_comment, 0)
        # 切换到目标文件夹所在的位置
        os.chdir(file_name)
        # 创建子文件夹的名称
        folder_name = 'sql'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        output_file = "{file_name}{folder_name}\\{source_name}_{source_table_name}-{target_table_name}.sql" \
            .format(file_name=file_name,folder_name=folder_name,source_name=source_name,source_table_name=source_table_name, target_table_name=target_table_name)
        # 追加写入文件
        with open(output_file, 'w',encoding='utf-8') as f1:
            result = '\n'.join([str(result) for result in query])
            f1.write("select \n{result} \nfrom {database_name}.{source_table_name}"
                     .format(result=result, database_name=database_name, source_table_name=source_table_name))
        f1.close()
