import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil

'''
TODO: 使用Resource Hacker将RES文件中的字符串提取出来生成rc文件
'''

s_UI_home = 'D:\\Pluswdev\\AM65A\\UISource'
s_runner_home = 'D:\\Software\\ResourceHacker'
s_RC_save_home = 'D:\\Pluswdev\\AM65A\\AM65AENG'

#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))

os.chdir(s_runner_home)

print('Step1:-----------直接从RES文件生成到另一个目录，并保持目录结构------', '-' * 50)

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
            print('s_convert_from: ', s_filepath)
            print('s_save_to: ', s_to_filepath, '.rc')
                        
            if not os.path.exists(s_to_folderpath):
                os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)
                
            #if os.path.exists(s_filepath):                
            fp = os.popen('ResourceHacker.exe -extract "%s", "%s.rc",  StringTable,,' % (s_filepath, s_to_filepath)) #路径用""引起来可以避免空格带来的问题
            fpread = fp.read()
            print(fpread)
            #shutil.copyfile(s_filepath, s_to_filepath)


'''
print('Step2:-----------Convert RES Files to RC-----------------------------------------------')

for root, dirs, files in os.walk(s_RC_save_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
    #print('Folder: ', root)
    for file in files:        
        s_filetype = os.path.splitext(file)[1].lower() #文件后缀
        #print(s_filetype)
        
        if (s_filetype == '.res')  :
            s_filepath = os.path.join(root, file)
            s_filename = os.path.join(root, os.path.splitext(file)[0]) #文件名
            print('s_Convert_from: ', s_filepath)
                        
            if os.path.exists(s_filepath):                
                fp = os.popen('ResourceHacker.exe -extract %s, %s.rc,  StringTable,,' % (s_filepath, s_filename)) #路径用""引起来可以避免空格带来的问题
                fpread = fp.read()
                print(fpread)
'''


