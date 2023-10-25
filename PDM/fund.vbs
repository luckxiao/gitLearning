'开始
Option Explicit

Dim mdl ' the current model
Set mdl = ActiveModel
If (mdl Is Nothing) Then
    MsgBox "There is no Active Model"
End If

Dim HaveExcel
Dim RQ
RQ = vbYes 'MsgBox("Is  Excel Installed on your machine ?", vbYesNo + vbInformation, "Confirmation")
If RQ = vbYes Then
    HaveExcel = True
    ' Open & Create  Excel Document
    Dim x1 '
    Set x1 = CreateObject("Excel.Application")
    x1.Workbooks.Open "D:\2023.10\基金\基金指数行情.xlsx" '指定 excel文档路径
    x1.Workbooks(1).Worksheets(1).Activate '默认打开第一个sheet
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
dim sheetIndex

on error Resume Next

For sheetIndex = 2 To 3              ' sheet的index
    With x1.Workbooks(1).Worksheets(sheetIndex)
        If .Cells(1, 1).Value = "" Then
                Exit For '跳出
        End If
        set table = mdl.Tables.CreateNew '创建表
        For rwIndex = 5 To 1000        'sheet 的行数
            If .Cells(rwIndex, 1).Value = "" Then
                Exit For
            End If
                    
            If rwIndex = 5 Then
                ' 表赋值
                table.Code=.Cells(2, 2).Value   '表名
                table.Name=.Cells(3, 2).Value   '表描述
                table.Comment=.Cells(4, 2).Value  '表备注
            Else        
                set col = table.Columns.CreateNew '创建一列/字段            
                
                col.Code = .Cells(rwIndex, 6).Value '指定表字段
                col.Name = .Cells(rwIndex, 7).Value '指定列名
                col.DataType = .Cells(rwIndex, 1).Value '指定列数据类型
                col.Comment = .Cells(rwIndex, 7).Value '指定列说明
                
                If .Cells(rwIndex, 2).Value = "N" Then
                    col.Mandatory = true '指定列是必填 true 为不可空 
                End If
                
                If .Cells(rwIndex, 3).Value = "Y" Then
                    col.Primary = true '指定主键
                End If
            End If        
        Next
    End With
Next

MsgBox "生成成功"

Exit Sub
End sub
