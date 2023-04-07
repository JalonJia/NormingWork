'''
Created on April 03, 2023
@author: Jalon Jia
'''

import sys
sys.path.append(r'd:\dev\NormingWork\src\Common')
import CreateRMPlusScriptByExcel
from datetime import date,datetime
import time





#Testing
if __name__ == '__main__' :
    #print(xlrd.XL_CELL_NUMBER)
    print('Start:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

    x = CreateRMPlusScriptByExcel.CreateRMPlusScriptByExcel(r'D:\Working\01WorkDocuments\OEMDocuments\RMPlusDocs\2023.01\Temp\RMPlus数据表设计-Jalon.xlsx')
    #x.read_excel()
    #x.read_excel_create_resource(r'D:\Working\02WeeklyWorking\0ThisWeek\temp.txt')
    s_saveto = r'D:\Working\02WeeklyWorking\0ThisWeek\Temp'
    x.generate_table_changes(s_saveto)
    # x.generate_security_changes(s_saveto)
    
    print('End:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
