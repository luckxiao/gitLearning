# @descripts:将excel转换成SQL查询的格式
# @time:2023.10.23
# @question:需要封装

import pandas as pd

# 拼接 SQL 中间的 格式
def read_m_data(columns_source,columns_targe,columns_comment,flag):

    if flag=='0':
        query.append("    {columns_source} as {columns_targe}, -- {columns_comment}" \
                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                             columns_comment=columns_comment))
    if flag=='1':
        query.append("    {columns_source} as {columns_targe} -- {columns_comment}" \
                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                             columns_comment=columns_comment))
# 获取一个sheet完整SQL
# def read_all_data(dict_data):

if __name__ == '__main__':
    database_name='WINDZX'
    # 读取excel文件,sheet_name=None 表示引用所有的sheet
    #df = pd.read_excel("D:\\20230515\\wind映射表.xlsx",sheet_name=[0,1])
    # 文件夹名称
    file_name='D:\\2023.10\\股票\\'
    dict_data = pd.read_excel(file_name + "股票-第一批stt-V1.xlsx", sheet_name=[1],
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
            columns_targe = row[3]  # 目标字段
            columns_comment = row[4]  # 目标注释
            if (index == sheet_len - 1):  # 如果为最后一行，则不加逗号
                columns_source = '\'' + str(source_table_name).upper() + '\'' + '||OBJECT_ID'  # object_id 为业务主键
                columns_targe = 'INC_ID_S'
                query.append("    {columns_source} as {columns_targe} -- {columns_comment}" \
                             .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                                     columns_comment=columns_comment))
            else:
                if (str(columns_targe).upper() == 'REC_IN_TAB_TIME' or str(
                        columns_targe).upper() == 'REC_UPT_TIME' or str(columns_targe).upper() == 'REC_ACHV_TIME'):
                    continue
                else:
                    if str(columns_targe).upper() == 'SRC_ID':
                        columns_source = '\'' + 'WIND.' + str(source_table_name).upper() + '\''
                        query.append("    {columns_source} as {columns_targe}, -- {columns_comment}" \
                                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                                             columns_comment=columns_comment))
                    elif str(columns_targe).upper() == 'DEL_FLAG':
                        columns_source = '\'' + '0' + '\''
                        query.append("    {columns_source} as {columns_targe}, -- {columns_comment}" \
                                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                                             columns_comment=columns_comment))
                    else:
                        query.append("    {columns_source} as {columns_targe}, -- {columns_comment}" \
                                     .format(columns_source=columns_source, columns_targe=str(columns_targe).strip(),
                                             columns_comment=columns_comment))
        # 文件输出路径
        output_file = file_name + "WIND_{source_table_name}-{target_table_name}.sql" \
            .format(source_table_name=source_table_name, target_table_name=target_table_name)
        # 追加写入文件
        with open(output_file, 'w') as f1:
            result = '\n'.join([str(result) for result in query])
            f1.write("select \n{result} \nfrom {database_name}.{source_table_name}"
                     .format(result=result, database_name=database_name, source_table_name=source_table_name))
        f1.close()
