
import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
from ReplaceInFile import replace_infile, copy_file

'''
TODO: 提供以下功能：
1. 将某个目录下面的VB界面代码复制到另一个目录下
2. 然后修改UI的Roto编号

主要过程：
a. 把以前的ROTO号全部替换为现在的ROTO号。例如：1094替换为6018
b. 在Dos窗口执行如下的命令，批量修改文件名：
E:\Pluswdev\EN61A\Source\Reports\Timesheet\PostingErrors\AccpacEN1094>
rename AccpacEN1094*.??? AccpacEN6018*.???
c. 打开vb的工程，打断兼容性，编译OCX和ENG.DLL .然后再与服务器兼容，可以当作新的UI来继续开发了。
'''

class CopyUIToNew(object):
    def __init__(self, s_from_path, s_to_path, s_new_ROTOID = ''):
        self.s_from_path = s_from_path
        self.s_to_path = s_to_path
        self.s_old_ROTOID = s_from_path[-4:]
        self.s_new_ROTOID = s_new_ROTOID
        if s_new_ROTOID == '':
            self.s_new_ROTOID = s_to_path[-4:]            
               
    def __copy_files(self):
        if not (os.path.exists(self.s_to_path)):
            os.makedirs(self.s_to_path, mode=0o777, exist_ok=True)

        for root, dirs, files in os.walk(self.s_from_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            for dir in dirs:
                s_to_dir = os.path.join(self.s_to_path, dir)
                if not (os.path.exists(s_to_dir)):
                    os.makedirs(s_to_dir, mode=0o777, exist_ok=True)
            
            for file in files:
                s_from_file = os.path.join(root, file)
                s_new_filename = file.replace(self.s_old_ROTOID, self.s_new_ROTOID) #修改文件名
                s_to_file = os.path.join(self.s_to_path, root[len(self.s_from_path): ], s_new_filename)
                copy_file(s_from_file, s_to_file)
                
                # with open(s_from_file, 'r', encoding='UTF-8', errors='ignore' ) as f_r:
                #     s_content = f_r.read()
                # with open(s_to_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
                #     f_w.write(s_content)


    def __replace_roto_in_files(self) :
        """
        TODO: 将目录下面.vbp和.vbg文件中的 s_old_ROTOID替换为 s_new_ROTOID
        """
        print('----------------------replace_roto_in_files------------------------------------')

        #replace from *.ctl and *.frm
        s_from_list = [f'EN{self.s_old_ROTOID}', r'CompatibleMode="\d"']
        s_to_list = [f'EN{self.s_new_ROTOID}', 'CompatibleMode="0"']

        for root, dirs, files in os.walk(self.s_to_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1] #文件后缀
                
                s_filepath = os.path.join(root, file)
                if (s_filetype in ['.vbp', '.vbg', '.bas', '.ctl', '.frm']):
                    replace_infile(s_filepath, s_from_list, s_to_list)
                

    def copy_and_modify(self):
        self.__copy_files()
        self.__replace_roto_in_files()
       

#Testing
if __name__ == '__main__' :
    s_copy_from = r'D:\Pluswdev\EN66A\VBSource\Requisitions\POInvoiceType\AccpacEN9165'
    s_copy_to = r'D:\Pluswdev\EN66A\VBSource\Requisitions\POReceiptType\AccpacEN9160'
    x = CopyUIToNew(s_copy_from, s_copy_to)
    x.copy_and_modify()

