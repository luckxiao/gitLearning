'******************************************************************************  
'* 所有的表设计都放在一个excel的一个sheet中，每个表中间空一行，表体都有表头说明如下，  
'* 再前面一行是表名和表的说明，分别在A和C列。下面格式直接拷贝到excel中就可以看到，空格是制表符。  
'******************************************************************************    
'                             Excel 格式如下 
'中文表名    英文表名    字段描述    英文字段    字段类型    字段说明    字段长度    主键    外键    是否为空    Precision                                     
'******************************************************************************    
Option Explicit  
  
Dim mdl ' the current model  
Set mdl = ActiveModel  
If (mdl Is Nothing) Then  
    MsgBox "There is no Active Model"  
End If  
  
Dim HaveExcel  
Dim RQ  
RQ = vbYes 'MsgBox("Is Excel Installed on your machine ?", vbYesNo + vbInformation, "Confirmation")  
If RQ = vbYes Then  
    HaveExcel = True  
    ' Open & Create Excel Document  
    Dim x1  '  
    Set x1 = CreateObject("Excel.Application")  
    x1.Workbooks.Open "D:\最闻\202407\股票基本信息&港股基本信息.xlsx"  '指定excel文档路径  
    x1.Workbooks(1).Worksheets(4).Activate   '指定要打开的sheet名称  
Else  
    HaveExcel = False  
End If  
  
a x1, mdl  
sub a(x1, mdl)  
dim rwIndex  
dim tableName  
dim colname  
dim table  
dim col  
dim count  
dim abc  
  
on error Resume Next  
'--------------------------------  
'下面是读取excel，添加表实体属性  
'--------------------------------  
For rwIndex = 2 To 1000  '指定要遍历的Excel行标  由于第2行是表头，从第1行开始，看你这个表设计多少行  
    With x1.Workbooks(1).Worksheets(4)'需要循环的sheet名称  
        If .Cells(rwIndex,1).Value <> "" And  .Cells(rwIndex,2).Value <> ""  Then  '第一列和第二列不为空，则创建表
            set table = mdl.Tables.CreateNew '创建一个表实体  
            table.Code = .Cells(rwIndex,2).Value'从excel中取得表名称、编码以及注释 
            table.Name = .Cells(rwIndex,1).Value
            table.Comment = .Cells(rwIndex,1).Value
            count = count + 1  
        End If 
		
        If .Cells(rwIndex,4).Value <>"" Then
            set col =table.Columns.CreateNew '创建一列/字段  
            col.Name = .Cells(rwIndex, 4).Value '指定列name  
            col.Code = .Cells(rwIndex, 3).Value '指定列code  
            col.DataType = .Cells(rwIndex, 9).Value '指定列数据类型 
            col.Comment =  .Cells(rwIndex, 4).Value '指定列说明   
            If .Cells(rwIndex, 11).Value = "y" or .Cells(rwIndex, 11).Value = "Y" Then'指定主键  
              col.Primary = true  
              End If       
            If .Cells(rwIndex, 10).Value = "n" or .Cells(rwIndex, 10).Value = "N" Then'指定列是否可空 true 为不可空  
             col.Mandatory = true  
             End If 
         End If  
    End With  
Next  
    MsgBox "生成数据表结构共计 " + CStr(count), vbOK + vbInformation, "表"  
Exit Sub  
End sub
