# Name     : thrdprty_and_nstrm.py
# Author   : Debasish
# Purpose  : For Upgrade thirdparty And Netstrome Build Upgrade, also Restart Tomcat Server

import os
import wget
import tarfile
import shutil
import paramiko
import logging
import time
import os.path
import glb

def Buildup():
    dire = os.getcwd()
    os.chdir(r"/home/cavisson/work/upgrade")
    print("     You just moved to the upgrade directory")
    new_dir = os.getcwd()
    print("And the current directory is ----" + new_dir)
    print("")

    print("     Starting Thirdparty build upgrade")
    key1 = "thirdparty."
    key2 = "_Ubuntu"
    key3 = "04_64.bin"
    key4 = "."
    finl = key1 + glb.buil + key4 + glb.buil1 + key2 + glb.ver + key3
    url1 = "http://10.20.0.82:8992/U" + glb.ver +"/"+ glb.buil + "/" + finl
    #print(url1)
    print('')
    print('thirdparty build download started')
    filename1 = wget.download(url1)
    print(filename1)
    print('')
    print("thirdparty Download Successfully")
    var1="chmod +x"+' '+finl
    os.system(var1)

    print('')
    print("     Starting netstrome_all build upgrade")
    key5 = "netstorm_all."
    finl1 = key5 + glb.buil + key4 + glb.buil1 + key2 + glb.ver + key3
    url2 = "http://10.20.0.82:8992/U" + glb.ver +"/"+ glb.buil + "/" + finl1
    print(url2)
    print('netstorm_all build download started')
    print('')
    filename2 = wget.download(url2)
    print(filename2)
    print('')
    print("netstorm_all Download Successfully")
    var2="chmod +x"+' '+finl1
    os.system(var2)
    
    print('')
    print('     execute thirdparty Build')
    print('')
    var3="./" + finl
    os.system(var3)
    print('')
    print("    execute netstorm_all Build")
    print('')
    var4="./" + finl1
    os.system(var4)
    print('')

    print("  -----Now Both Netstrom and thirdparty upgraded to " + glb.buil+key4+glb.buil1 +"-----")
    print("")
    print('')
    print(" ----Here is the details Build Verison----")
    print('')
    os.system("nsu_get_version")
    print('')
    print('---Successfully completed netstrom and thirdparty upgrade process')

def Tomcat():
    print('')
    print("         --Restart tomcat server--")
    print('')
    tom = "/etc/init.d/tomcat"+' '+"restart"
    os.system(tom)
    print("Tomcat restart successfully completed")



#Tomcat()
#Buildup()
