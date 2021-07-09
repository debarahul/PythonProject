# Name     : nfdb_ui_and_nodesrv.py
# Author   : Debasish
# Purpose  : For Upgrade NFUI, NFDB And Nodeserver

import wget
import tarfile
import os
import shutil
import paramiko
import logging
import time
import glb

key1 = "."
key2 = ".tar.gz"
rootPassword = 'cavisson'
rootuser = 'cavisson'

def Nfdb_BuildUpd():
    dire = os.getcwd()
    os.chdir(r"/home/cavisson/work/debasish/nfdb742/mltesting/")
    print("     You just moved to the new directory for NFDB upgrade")
    new_dir = os.getcwd()
    print("And the current directory is ----" + new_dir)
    print("")

    print('')
    print("        Now Starting NFDB Build Upgrade")
    print('')
    key = "nfdb742-"
    fnl = key + glb.buil + key1 + glb.buil1

    if os.path.exists(fnl + key2):
        os.remove(fnl + key2)
    else:
        print("cant Delete file as it doesnt exist in the current directory")

    url = "http://10.20.0.82:8992/others/NETFOREST/" + fnl + key2
    print("Starting NFDB Build Download")
    print('')
    try:
        filename = wget.download(url)
        print(filename)
        print("Build Download Successfully")
        tar = tarfile.open(filename, 'r')
        ext_tar = tar.extractall()
        print("build is succesfully untared")
        new = os.getcwd()
        os.chdir(r"/home/cavisson/work/lrm/nfdb742/" + fnl + "/config")

        if os.path.exists('lookup'):
            shutil.rmtree('lookup')
        else:
            print('cant Delete file as it doesnt exist in the current directory')
        print('')
        print("Now i am creating lookup directory")
        print('')
        lukup = "lookup"
        dest = new_dir +"/"+fnl+"/config/"
        path = os.path.join(dest, lukup)
        #os.mkdir(path)
        shutil.copytree('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/lookup', path)
        shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/nfdb.yml', dest)
        shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/log4j2.properties', dest)
        shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/jvm.options', dest)

        os.chdir(r"/home/cavisson/work/debasish/nfdb742/mltesting/"+fnl+"/bin/")
        new1_dir = os.getcwd()
        print(new1_dir)
        #os.system("echo $JAVA_HOME$")
        os.environ["JAVA_HOME"] = "/home/cavisson/work/debasish/jdk-12"
        #os.system("echo $JAVA_HOME$")
        cmd = "./nfdb -d"
        os.system(cmd)
        print('')
        print("--- Now the NFDB Upgraded Successfully---")
    except Exception:
        print('')
        print('The 742-NFDB build you want to download is not available on bildub, else you have entered wrong input')
        print('')


#Nfdb_BuildUpd()

def Nfui_upd():
    print('')
    dire1 = os.getcwd()
    os.chdir(r"/home/cavisson/work/debasish/nfdb742/mltesting/ui")
    print("       You just moved to the new directory for NFUI upgrade")
    new_dir1 = os.getcwd()
    print("And the current directory is ----" + new_dir1)

    print('')
    print("           Now Starting NFUI Build Upgrade")
    print('')
    
    key3 = "NetForest-UI-"
    key4 = ".tar"
    fnl1 = key3 + glb.buil + key1 + glb.buil1

    if os.path.exists(fnl1 + key4):
        os.remove(fnl1 + key4)
    else:
        print("cant Delete file as it doesnt exist in the current directory")

    url1 = "http://10.20.0.82:8992/others/NETFOREST/" + fnl1 + key4
    print("Starting NFDB Build Download")
    print('')
    filename1 = wget.download(url1)
    print(filename1)
    print("--Build Download Successfully--")

    if os.path.exists('NetForest-UI'):
        shutil.rmtree('NetForest-UI')
    else:
        print('')
        print("cant Delete file as it doesnt exist in the current directory")
        print('')

    tar1 = tarfile.open(filename1, 'r')
    ext_tar1 = tar1.extractall()
    print("build is succesfully untared")
    conf_js = new_dir1 + "/NetForest-UI/NetForest-Unified/assets/Config"
    conf_ser = new_dir1 + "/NetForest-UI/server/config"
    shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/config.json', conf_js)
    shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/config.yml', conf_ser)

    os.chdir(r"/home/cavisson/work/debasish/nfdb742/mltesting/ui/NetForest-UI/bin")
    perms = "chmod +x"+' '+"NetForestStart.sh"
    os.system(perms)

    cmd = 'sh NetForestStart.sh'
    os.system('echo %s|sudo -su %s -S %s' % (rootPassword, rootuser, cmd))
    print('')
    print("--- Now the old-742-NFUI Upgraded Successfully---")
    print('')


#Nfui_upd()


def node_serv_upd():
    print('')
    os.chdir(r'/home/cavisson/work/debasish/nodeserver/')
    print("       You just moved to the new directory for nodeserver upgrade")
    new_dir2 = os.getcwd()
    print("And the current directory is ----" + new_dir2)
    
    print('')
    print("           Now Starting nodeserver Build Upgrade")
    print('')

    key5 = "UnifiedLogServer-"
    fnl2 = key5 + glb.buil + key1 + glb.buil1

    if os.path.exists(fnl2 + key2):
        os.remove(fnl2 + key2)
    else:
        print("cant Delete file as it doesnt exist in the current directory")

    url2 = "http://10.20.0.82:8992/others/NETFOREST/" + fnl2 + key2
    #print(url2)
    try:
        print("            Starting nodeserver Build Download")
        print('')
        filename2 = wget.download(url2)
        print(filename2)
        print("--Build Download Successfully--")

        if os.path.exists('LogMonServer'):
            shutil.rmtree('LogMonServer')
        else:
            print('')
            print("cant Delete file as it doesnt exist in the current directory")
            print('')
    
        tar2 = tarfile.open(filename2, 'r')
        ext_tar2 = tar2.extractall()
        print("nodeserver build is succesfully untared")

        deflt_js = new_dir2 + '/LogMonServer/UnifiedServer/config'
        shutil.copy('/home/cavisson/work/debasish/nfdb742/mltesting/filedetl_fr_auto/default.json', deflt_js)
        os.chdir(r"/home/cavisson/work/debasish/nodeserver/LogMonServer/UnifiedServer/bin/")
        permsn = "chmod +x"+' '+"StartServer.sh"
        os.system(permsn)
        cmd1 = './StartServer.sh'
        os.system('echo %s|sudo -su %s -S %s' % (rootPassword, rootuser, cmd1))
        print('')
        print("--- Now the nodeserver Upgraded Successfully---")
        print('')
    except Exception:
        print('')
        print('The build you want to download is not available on bildub, For this build you have to ping in build group')
        print('')

#node_serv_upd()




