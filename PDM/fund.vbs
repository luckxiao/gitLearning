'��ʼ
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
    x1.Workbooks.Open "D:\2023.10\����\����ָ������.xlsx" 'ָ�� excel�ĵ�·��
    x1.Workbooks(1).Worksheets(1).Activate 'Ĭ�ϴ򿪵�һ��sheet
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

For sheetIndex = 2 To 3              ' sheet��index
    With x1.Workbooks(1).Worksheets(sheetIndex)
        If .Cells(1, 1).Value = "" Then
                Exit For '����
        End If
        set table = mdl.Tables.CreateNew '������
        For rwIndex = 5 To 1000        'sheet ������
            If .Cells(rwIndex, 1).Value = "" Then
                Exit For
            End If
                    
            If rwIndex = 5 Then
                ' ��ֵ
                table.Code=.Cells(2, 2).Value   '����
                table.Name=.Cells(3, 2).Value   '������
                table.Comment=.Cells(4, 2).Value  '��ע
            Else        
                set col = table.Columns.CreateNew '����һ��/�ֶ�            
                
                col.Code = .Cells(rwIndex, 6).Value 'ָ�����ֶ�
                col.Name = .Cells(rwIndex, 7).Value 'ָ������
                col.DataType = .Cells(rwIndex, 1).Value 'ָ������������
                col.Comment = .Cells(rwIndex, 7).Value 'ָ����˵��
                
                If .Cells(rwIndex, 2).Value = "N" Then
                    col.Mandatory = true 'ָ�����Ǳ��� true Ϊ���ɿ� 
                End If
                
                If .Cells(rwIndex, 3).Value = "Y" Then
                    col.Primary = true 'ָ������
                End If
            End If        
        Next
    End With
Next

MsgBox "���ɳɹ�"

Exit Sub
End sub
