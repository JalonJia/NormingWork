import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import RESTool
import ReplaceInFile
import BingTrans
import time

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
    def copyAndChangeLanguage(s_UI_home, s_RC_save_home, s_to_Lang='ENG'):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filename2 = s_filename.upper()
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filename)

                if (s_filename=='Localizer' or (s_filetype == '.vbp' and s_filename2.endswith('ENG'))):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RC_save_home + s_relative_path  #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filename = s_filename
                    if (s_filetype == '.vbp' and s_filename2.endswith('ENG')):
                        s_to_filename = s_filename[:-3] + s_to_Lang
                    s_to_filepath = os.path.join(s_to_folderpath, s_to_filename+s_filetype)
                    print('s_copy_from: ', s_filepath, f's_save_to: {s_to_filepath}')                    

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)

                    shutil.copyfile(s_filepath, s_to_filepath)

                    if (s_filetype == '.vbp') and (s_filename2.endswith('ENG')) and (s_to_Lang!='ENG'):
                        ReplaceInFile.replace_infile(s_to_filepath, ['ENG'], [s_to_Lang])



    @staticmethod
    def convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home, s_to_Lang='ENG'):
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
                    #print('s_convert_from: ', s_filepath)
                    #print(f's_save_to: {s_to_filepath}.rc')

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)

                    RES_util = RESTool.RESTool(s_runner_home)
                    RES_util.convertRESToRC(s_filepath, s_to_folderpath, s_to_Lang)


    @staticmethod
    def translateRCtoLang(s_runner_home, s_UI_home, s_RES_save_home, s_to_lang):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)

                if ((s_filetype == '.rc') and (s_filename.endswith('_ori')) and (not s_filename.endswith('icon_ori'))):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RES_save_home + s_relative_path #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, file.replace('_ori', ''))

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)
                    
                    if os.path.exists(s_to_filepath): #已经创建过的旧不再创建了
                        continue

                    print('Working on: %s' % s_to_filepath)

                    encode_file = 'utf-16 le'
                    translate = BingTrans.BingTrans()
                    translate.translateOneFile('en', s_to_lang, s_fromfile=s_filepath, s_tofile=s_to_filepath, encode_from = encode_file, encode_to = encode_file)



    @staticmethod
    #翻译View的ENG文件，文件编码不同
    def translateViewRCtoLang(s_runner_home, s_UI_home, s_RES_save_home, s_to_lang):
        for root, dirs, files in os.walk(s_UI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)

                if ((s_filetype == '.rc') or (s_filetype == '.rci')):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_RES_save_home + s_relative_path #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, file)

                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)
                    
                    if os.path.exists(s_to_filepath): #已经创建过的旧不再创建了
                        continue

                    print('Working on: %s' % s_to_filepath)

                    encode_read = 'utf-8'
                    if s_filetype == '.rci':
                        encode_read = 'GBK'

                    translate = BingTrans.BingTrans()
                    translate.translateOneFile('en', s_to_lang, s_fromfile=s_filepath, s_tofile=s_to_filepath, encode_from = encode_read, encode_to = 'utf-8')
                                                                                

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

                if ((s_filetype == '.rc') and (not s_filename.endswith('_ori')) and (not s_filename.endswith('icon'))):
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
                    

'''
TODO: Testing
'''
if __name__ == '__main__' :
    s_runner_home = r'D:\Dev\ResourceHacker'
    s_UI_home = r'D:\Pluswdev\EN69A\VBSource' 
    s_RC_save_home = r'D:\Pluswdev\EN69A\EN69AFRA'
    #s_RC_save_home = r'D:\Pluswdev\EN69A\EN69AFRA\Billing\BillingAnalysis'

    s_ViewRC_home = r'D:\Pluswdev\EN69A\Source\Cprogram\Eng' 
    s_ViewRC_Save_To = r'D:\Pluswdev\EN69A\EN69AFRA\CPROGRAM\Fra'
    
    #s_UI_home = r'D:\Pluswdev\AM66A\AM66AFRA\Setup\Accsets' 
    #s_RC_save_home = r'D:\Working\WeeklyWorking\0ThisWeek'

    #CopyENGProject.copyAndChangeLanguage(s_UI_home, s_RC_save_home, 'FRA')
    #CopyENGProject.convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home, 'FRA')
    #CopyENGProject.translateRCtoLang(s_runner_home, s_RC_save_home, s_RC_save_home, 'fr')
    #CopyENGProject.translateViewRCtoLang(s_runner_home, s_ViewRC_home, s_ViewRC_Save_To, 'fr')
    translate = BingTrans.BingTrans()
    translate.translateOneFile('en', 'fr', s_fromfile=r'D:\Pluswdev\EN69A\EN69AFRA\GrpDefs\Grp.txt', s_tofile=r'D:\Pluswdev\EN69A\EN69AFRA\GrpDefs\Grp_Fra.txt', encode_from = 'GBK', encode_to = 'utf-8')  
    #CopyENGProject.convertRCToRES(s_runner_home, s_RC_save_home, s_RC_save_home)
