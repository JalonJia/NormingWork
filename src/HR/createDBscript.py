'''
Created on May 23, 2018
@author: Jalon Jia
'''

import sys
sys.path.append(r'd:\dev\NormingWork\src\Common')
import CreateHRScriptByExcel
from datetime import date,datetime
import time





#Testing
if __name__ == '__main__' :
    #print(xlrd.XL_CELL_NUMBER)
    print('Start:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

    #x = CreateHRScriptByExcel(r'D:\Working\WorkDocuments\OEMDocuments\HRMSDocs\2021.09\eHRMS2021.09数据流.xlsx')
    #x = CreateHRScriptByExcel.CreateHRScriptByExcel(r'D:\Working\01WorkDocuments\OEMDocuments\HRMSDocs\2023.12\eHRMS数据表改动2023.12.xlsx')
    #x = CreateHRScriptByExcel.CreateHRScriptByExcel(r'D:\Working\02WeeklyWorking\0ThisWeek\eHRMS数据表改动22.08.xlsx')
    x = CreateHRScriptByExcel.CreateHRScriptByExcel(r'D:\Working\01WorkDocuments\OEMDocuments\HRMSDocs\Customizations\CIDRZ\eHRMS数据表改动CIDRZ.xlsx')
    #x.read_excel()
    #x.read_excel_create_resource(r'D:\Working\02WeeklyWorking\0ThisWeek\temp.txt')
    s_saveto = r'D:\Working\02WeeklyWorking\0ThisWeek\Temp'
    x.generate_table_changes(s_saveto)
    x.generate_security_changes(s_saveto)
    
    print('End:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
