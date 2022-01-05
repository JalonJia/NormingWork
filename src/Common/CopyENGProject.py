import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import RESTool

'''
TODO: 使用Resource Hacker将RES文件中的字符串提取出来生成rc文件
'''

# s_UI_home = 'D:\\Pluswdev\\AM65A\\UISource'
# s_runner_home = 'D:\\Software\\ResourceHacker'
# s_RC_save_home = 'D:\\Pluswdev\\AM65A\\AM65AENG'

#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))


class CopyENGProject(object):
    def __init__(self):
        pass
    
    @staticmethod
    def copyFiles(s_UI_home, s_RC_save_home):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filename2 = s_filename.lower()
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filename)

                if (s_filename=='Localizer' or (s_filetype == '.vbp' and s_filename2.endswith('eng'))):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RC_save_home + s_relative_path  #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, s_filename+s_filetype)
                    print('s_copy_from: ', s_filepath, f's_save_to: {s_to_filepath}')                    

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)

                    shutil.copyfile(s_filepath, s_to_filepath)


    @staticmethod
    def convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)

                if (s_filetype == '.res'):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RC_save_home + s_relative_path #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, os.path.splitext(file)[0])
                    s_to_filepath_CHN = os.path.join(s_to_folderpath, os.path.splitext(file)[0].replace('ENG', 'CHN'))
                    #print('s_convert_from: ', s_filepath)
                    #print(f's_save_to: {s_to_filepath}.rc')

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)

                    RES_util = RESTool.RESTool(s_runner_home)
                    RES_util.convertRESToRC(s_filepath, s_to_folderpath)
                    

    @staticmethod
    def convertRCToRES(s_runner_home, s_UI_home, s_RES_save_home):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)

                if ((s_filetype == '.rc') and (not s_filename.endswith('icon'))):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RES_save_home + s_relative_path #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, os.path.splitext(file)[0])
                    #s_to_filepath_CHN = os.path.join(s_to_folderpath, os.path.splitext(file)[0].replace('ENG', 'CHN'))
                    #print('s_convert_from: ', s_filepath)
                    #print(f's_save_to: {s_to_filepath}.rc')

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)

                    RES_util = RESTool.RESTool(s_runner_home)
                    RES_util.convertRCToRES(s_filepath, s_to_folderpath)
                    

