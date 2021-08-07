# Author Debasish
import os
import wget
import tarfile
import shutil
import paramiko
import logging
import time
import os.path

print("")
print("       It’s automation, not automagic")
print('')
print("     ------Let's start our task-----")
print('')


def Buildup():
    dire = os.getcwd()
    print(dire)
    os.chdir(r"/home/cavisson/work/upgrade")
    print("     You just moved to the upgrade directory")
    new_dir = os.getcwd()
    # print(new_dir)
    print("")
    buil = input("Don't shy, Give me Version number what you want to download: ")
    print(buil)
    buil1 = input("Enter the Build number. Share it fast, we dont have much time: ")
    print(buil1)
    ver = input("Share your OS Release Details in number format: ")
    print(ver)
    key1 = "thirdparty."
    key2 = "_Ubuntu"
    key3 = "04_64.bin"
    key4 = "."
    finl = key1 + buil + key4 + buil1 + key2 + ver + key3
    print(finl)
    url1 = "http://10.20.0.82:8992/U" + ver + "/" + buil + "/" + finl
    print(url1)
    filename1 = wget.download(url1)
    print(filename1)
    print("thirdparty Download Successfully")
    var1 = "chmod +x" + ' ' + finl
    os.system(var1)

    print('')
    print("Starting netstrome_all build upgrade")
    key5 = "netstorm_all."
    finl1 = key5 + buil + key4 + buil1 + key2 + ver + key3
    print(finl1)
    url2 = "http://10.20.0.82:8992/U" + ver + "/" + buil + "/" + finl1
    print(url2)
    filename2 = wget.download(url2)
    print(filename2)
    print("netstorm_all Download Successfully")
    var2 = "chmod +x" + ' ' + finl1
    os.system(var2)

    print('')
    print('     execute thirdparty Build')
    print('')
    var3 = "./" + finl
    os.system(var3)
    print('')
    print("    execute netstorm_all Build")
    print('')
    var4 = "./" + finl1
    os.system(var4)
    print('')

    print("  -------Now Both Netstrom and thirdparty upgrade with " + buil + key4 + buil1)
    print("")
    print("    ------Here is the details Build Verison")
    os.system("nsu_get_version")
    print("")
    print("   Thanku Have a Good Day. I know you can do it,jst beliave in yourself")
    print('')


Buildup()
