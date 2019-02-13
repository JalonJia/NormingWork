import os
import os.path
from os.path import join 
import ReplaceInFile

#sPath = "D:\ACCPAC\AM65A"
#print(os.listdir(sPath))
#Test Funtions
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))
#os.makedirs(path) #创建多级目录

def get_project_list(s_scource_folder, s_module) :
    l_count = 0
    s_projects = []

    for root, dirs, files in os.walk(s_scource_folder): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        #print('Folder: ', root)
        for dir in dirs:
            s_dirname = os.path.split(dir)[1].upper()
            if s_dirname[:2].lower() == s_module.lower():
                s_project = 'Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "%s", "%s\%s.vcproj", "{087BCF37-96BD-4624-B6E0-645E1722E6ED}"\nEndProject\n' % (s_dirname, s_dirname, s_dirname.lower())
                s_projects.append(s_project)

    return s_projects          

 

def generate_sln_file(s_file_path, s_module, file_encoding='UTF-8') :
    '''
        TODO：生成sln文件
    '''
    s_gen_file = os.path.join(s_file_path, f'{s_module}ALL.sln')
    # s_file_path = s_file_path.replace('.vbp', '_new.vbp')
    with open(s_gen_file, 'w', encoding=file_encoding, errors='ignore' ) as f_w:
        f_w.write('\nMicrosoft Visual Studio Solution File, Format Version 9.00\n')
        f_w.write('# Visual Studio 2005\n')

        s_projects = get_project_list(s_file_path, s_module)
        for project in s_projects:
            f_w.write(project)

        f_w.write('Global\n')
        f_w.write('\tGlobalSection(SolutionConfigurationPlatforms) = preSolution\n')
        f_w.write('\t\tDebug|Win32 = Debug|Win32\n')
        f_w.write('\t\tRelease|Win32 = Release|Win32\n')
        f_w.write('\tEndGlobalSection\n')
        f_w.write('\tGlobalSection(SolutionProperties) = preSolution\n')
        f_w.write('\t\tHideSolutionNode = FALSE\n')
        f_w.write('\tEndGlobalSection\n')
        f_w.write('\tEndGlobal\n')        


if __name__ == '__main__':
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\AQ66A\ViewSource', 'AQ')
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\BS66A\ViewSource', 'BS')
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\SS66A\ViewSource', 'SS')
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\VS66A\ViewSource', 'VS')
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\IS66A\ViewSource', 'IS')
    generate_sln_file(r'D:\Pluswdev2012\Security\Sec2019\PS66A\ViewSource', 'PS')

