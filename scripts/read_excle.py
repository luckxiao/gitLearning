import pandas as pd

database_name='WINDZX'
# 读取excel文件,sheet_name=None 表示引用所有的sheet
#df = pd.read_excel("D:\\20230515\\wind映射表.xlsx",sheet_name=[0,1])
# 文件夹名称
file_name='D:\\2023.10\\股票\\'

df = pd.read_excel(file_name+"股票-第一批stt-V1.xlsx",sheet_name=[1,2],skiprows=4) # skiprows 跳过前第四行，sheet_name 索引从0开始，前闭后闭
for sheet_num in list(df.keys()):
    #获取目标表名称
    target_table_name=df[sheet_num]['目标表名称'][1]
    source_table_name=df[sheet_num]['来源表名'][2]
    # 文件输出路径
    output_file = file_name+"WIND_{source_table_name}-{target_table_name}.sql"\
        .format(source_table_name=source_table_name,target_table_name=target_table_name)
    query=[]
    for index,row in df[sheet_num].iterrows():
        columns_source=row[9]      # 源字段
        columns_targe=row[3]       # 目标字段
        columns_comment=row[4]     # 目标注释
        query.append("{columns_source} as {columns_targe}, -- {columns_comment}"\
            .format(columns_source=columns_source,columns_targe=str(columns_targe).strip(),columns_comment=columns_comment))
    #追加写入文件
    with open(output_file,'w') as f1:
        result = ',\n'.join([str(result) for result in query])
        f1.write("select \n{result} \nfrom {database_name}.{source_table_name}"
                 .format(result=result,database_name=database_name,source_table_name=source_table_name))
    f1.close()





