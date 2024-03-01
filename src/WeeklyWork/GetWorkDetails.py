'''
Created on May 23, 2018
To Read Excel
@author: Jalon Jia
'''

from src.Common.TableClass import Field, Table
import xlrd  # 安装包：pip install xlrd
from datetime import date, datetime
import src.Common.ReplaceInFile
import os
import copy
from src.Common.TaskType import *


class ReadExcel(object):
    '''
    classdocs
    '''

    def __init__(self, p_file_folder):
        '''
        Constructor
        '''
        self.excel_folder = p_file_folder

    def __get_workdetails_from_excel(self, file_name):
        '''
        读取Excel，得到一周每个人的工作内容及时间
        '''

        labors = []
        labor = Labor('')

        # 文件位置
        ExcelFile = xlrd.open_workbook(file_name)

        # 获取目标EXCEL文件sheet名
        # print('Sheets:', ExcelFile.sheet_names())

        # ------------------------------------
        # 若有多个sheet，则需要指定读取目标sheet例如读取sheet2
        # sheet2_name=ExcelFile.sheet_names()[1]
        # ------------------------------------
        # 获取sheet内容【1.根据sheet索引2.根据sheet名称】
        # sheet=ExcelFile.sheet_by_index(1)
        sheet = ExcelFile.sheet_by_index(1)
        if sheet.name=='20220318':
            sheet = ExcelFile.sheet_by_index(2)
        # 打印sheet的名称，行数，列数
        # print('Sheet Name:%s, Rows: %d, Columns: %d' % (sheet.name, sheet.nrows, sheet.ncols))
        # 1A：Resource	2B：Line No.	3C：Task	4D：预计小时数	5E：预计完成日期
        # 6F：完成状态	7G:实际工作小时数	8H：实际完成日期	9I:Comments

        # print Each Cell
        for row in range(sheet.nrows):
            s_labor = str(sheet.row_values(row)[0]).strip()  # A列是姓名
            if s_labor == 'Resource' or row == 0:
                continue

            if (len(s_labor) > 0
                    and not '其' in s_labor
                    and not '外' in s_labor
                    and not '调' in s_labor):
                if labor.labor_name > '':
                    last_labor = copy.deepcopy(labor)
                    labors.append(last_labor)

                labor.labor_name = sheet.row_values(row)[0].strip()
                labor.plan_hours = 0
                labor.tasks = []
                continue

            if len(str(sheet.row_values(row)[2]).strip()) == 0:
                continue

            task = Task()

            if sheet.row_values(row)[1].strip() > '':
                task.seq = sheet.row_values(row)[1].strip()

            task.desc = str(sheet.row_values(row)[2]).strip().replace("\n", '   ').replace('\r','')
            task.comment = str(sheet.row_values(row)[8]).strip().replace("\n", '   ').replace('\r','')
            if len(str(sheet.row_values(row)[3]).strip()) > 0:
                task.plan_hours = float(sheet.row_values(row)[3])
            else:
                task.plan_hours = 0

            # print('PlanDate:', sheet.row_values(row)[4])
            if len(str(sheet.row_values(row)[4]).strip()) > 0:
                task.plan_date = datetime.fromordinal(
                    int(sheet.row_values(row)[4]) + datetime(1900, 1, 1).toordinal() - 2)
            else:
                task.plan_date = datetime(int(sheet.name[:4]), int(sheet.name[4:6]), int(sheet.name[6:]))

            s_status = str(sheet.row_values(row)[5]).strip()
            if s_status == 'Y':
                task.status = TaskStatus.STATUS_COMPLETED
            elif s_status == 'N':
                task.status = TaskStatus.STATUS_NOTCOMP
            elif s_status == 'P':
                task.status = TaskStatus.STATUS_PENDING
            else:
                task.status = TaskStatus.STATUS_NA

            # print(sheet.row_values(row)[6])
            if len(str(sheet.row_values(row)[6]).strip()) > 0:
                task.actual_hours = float(sheet.row_values(row)[6])
            else:
                task.actual_hours = 0

            # print('EndDate:', sheet.row_values(row)[7])
            if len(str(sheet.row_values(row)[7]).strip()) > 0:
                task.end_date = datetime.fromordinal(
                    int(sheet.row_values(row)[7]) + datetime(1900, 1, 1).toordinal() - 2)
            else:
                task.end_date = datetime(int(sheet.name[:4]), int(sheet.name[4:6]), int(sheet.name[6:]))

            if 'PSA' in task.desc.upper():
                task.product = Product.PRODUCT_PSA
            elif 'HR' in task.desc.upper():
                task.product = Product.PRODUCT_HR
            elif 'payroll' in task.desc.lower() or 'NP' in task.desc.upper():
                task.product = Product.PRODUCT_NP
            elif 'AM' in task.desc.upper():
                task.product = Product.PRODUCT_AM
            elif 'RM+' in task.desc.upper() or 'RM PLUS' in task.desc.upper() or 'RM +' in task.desc.upper():
                task.product = Product.PRODUCT_RMPLUS
            elif 'SECURITY' in task.desc.upper():
                task.product = Product.PRODUCT_SECURITY
            else:
                task.product = Product.PRODUCT_RM

            if '测试' in task.desc or 'test' in task.desc.lower():
                task.task_class = TaskClass.TASK_TEST
            elif 'customization' in task.desc.lower() or '客户化' in task.desc:
                task.task_class = TaskClass.TASK_CUSTMZ
            elif '管理' in task.desc:
                task.task_class = TaskClass.TASK_MANAGER
            elif 'helpdesk' in task.desc.lower() or '支持' in task.desc:
                task.task_class = TaskClass.TASK_SUPPORT

            labor.add_task(task)

        # 最后一个table
        if labor.labor_name > '':
            last_labor = copy.deepcopy(labor)
            labors.append(last_labor)

        return labors

    def generate_workdetails(self, file_path):
        '''
        得到，并打印出来
        '''

        labors_list = []

        for root, dirs, files in os.walk(self.excel_folder):  # files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            # print('Folder: ', root)
            # s_relative_path = root[len(s_UI_home): ]
            # print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0]  # 文件名
                s_filetype = os.path.splitext(file)[1].lower()  # 文件后缀
                # print(s_filetype)

                if (s_filetype == '.xlsx'):
                    s_filepath = os.path.join(root, file)
                    labors = self.__get_workdetails_from_excel(s_filepath)
                    if len(labors) > 0:
                        labors_list.append(labors)

        if len(labors_list) == 0:
            return

        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)

        s_file = os.path.join(file_path, 'WorkSummary.txt')
        with open(s_file, 'w', encoding='UTF-8', errors='ignore') as f_w:
            for labors in labors_list:
                for labor in labors:
                    f_w.write(labor.get_labor_sqlscript())


# Testing
if __name__ == '__main__':
    # print(xlrd.XL_CELL_NUMBER)
    x = ReadExcel(r'D:\Working\02WeeklyWorking\2023\2023Weekly')
    # x = ReadExcel(r'D:\Working\02WeeklyWorking\2023\test')
    # x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM66A\PU2\Design\EN66A_PU2_TablesChange.xlsx')
    # x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM67A\PU0\Design\POTables.xlsx')
    # x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    x.generate_workdetails(r'D:\Working\02WeeklyWorking\2023')
