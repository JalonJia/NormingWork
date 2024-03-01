'''
提供以下功能：
1. 定义日常任务数据结构
2.
3.
'''
from enum import Enum
from os import replace
from re import split, sub
from datetime import date, datetime
import time


class Product(Enum):
    '''
    产品列表
    '''
    PRODUCT_RM = 'RM'
    PRODUCT_HR = 'HR'
    PRODUCT_AM = 'AM'
    PRODUCT_NP = 'NP'
    PRODUCT_PSA = 'PSA'
    PRODUCT_SECURITY = 'SECURITY'
    PRODUCT_RMPLUS = 'RM+'


class TaskClass(Enum):
    '''
    任务类型
    '''
    TASK_DEV = 'Develop'
    TASK_TEST = 'Testing'
    TASK_SUPPORT = 'Support'
    TASK_MANAGER = 'Management'
    TASK_CUSTMZ = 'Customization'


class TaskStatus(Enum):
    '''
    任务类型
    '''
    STATUS_COMPLETED = 'Completed'
    STATUS_NA = 'Not Do'
    STATUS_PENDING = 'Pending'
    STATUS_NOTCOMP = 'Not Completed'


class Task(object):
    '''
    定义任务
    '''

    def __init__(self, s_product=Product.PRODUCT_RM, s_task_class=TaskClass.TASK_DEV,
                 s_desc='', s_comment='',
                 dt_plan_date=datetime.now(), dt_end_date=datetime.now(),
                 d_plan_hours=0.0, d_actual_hours=0.0,
                 i_status=TaskStatus.STATUS_COMPLETED):
        self.product = s_product
        self.task_class = s_task_class
        self.plan_date = dt_plan_date
        self.end_date = dt_end_date
        self.desc = s_desc
        self.comment = s_comment
        self.plan_hours = d_plan_hours
        self.actual_hours = d_actual_hours
        self.status = i_status
        self.seq = 0

    def __str__(self):
        '''
        生成与以下标题对齐的字符串
        ##___C-name______C-type______name________type_____elements_____________decimals____validator_____presents_____________flags__________attributes_____________
        '''

        str = ''
        return str


class Labor(object):
    '''
    定义Labor的数据结构
    '''

    def __init__(self, s_labor_name: str, d_plan_hours=0.0, d_actual_hours=0.0):
        '''
        Constructor
        '''
        self.labor_name = s_labor_name
        self.plan_hours = d_plan_hours
        self.actual_hours = d_actual_hours
        self.tasks = []

    def add_task(self, task):
        '''
        增加字段
        '''
        self.tasks.append(task)

    def remove_task(self, task_desc):
        '''
        删除字段
        '''
        for f in self.tasks[:]:
            if f.desc == task_desc:
                self.tasks.remove(f)

    def get_labor_tasks(self):
        '''
        得到某个人所有任务列表
        '''

        s_tbl = '#___C-name______C-type______name________type_____elements_____________decimals____validator_____presents_____________flags__________attributes_____________\n'

        for task in self.tasks:
            s_tbl += str(task)
            s_tbl += '\n'
        return s_tbl

    def get_labor_sqlscript(self):
        '''
        得到SQL语句
        INSERT INTO [OEMTASKS]([UUID], [RESOURCE], [TASK], [WEEKSEQ], [PLANDATE], [PLANHOUR], [ENDDATE], [ACTUALHOUR], [PRODUCT], [TASKCLASS], [STATUS], [COMMENT])
         VALUES ('uuid1', N'Jalon', N'task', N'1', '2023-10-01', 4.000, '2023-10-02', 6.000, N'RM', N'Dev', N'Completed', N'好');
        '''

        if len(self.tasks) == 0:
            return ''

        s_script = ''

        for task in self.tasks:
            s_script += (
                'INSERT INTO [OEMTASKS]([UUID], [RESOURCE], [TASK], [WEEKSEQ], [PLANDATE], [PLANHOUR], [ENDDATE],'
                ' [ACTUALHOUR], [PRODUCT], [TASKCLASS], [STATUS], [COMMENT]) \n'
                'VALUES ( NEWID(), ')

            s_script += "N'%s', N'%s', N'%s', '%s', %.3f, '%s', %.3f, N'%s', N'%s', N'%s', N'%s'" % (
                self.labor_name, task.desc, task.seq, task.plan_date.strftime("%Y-%m-%d"), task.plan_hours,
                task.end_date.strftime("%Y-%m-%d"), task.actual_hours, task.product.value, task.task_class.value,
                task.status.value,
                task.comment)

            s_script += ');\n'

        return s_script
