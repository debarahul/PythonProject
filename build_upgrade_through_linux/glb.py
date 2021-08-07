# Name     : glb.py
# Author   : Debasish
# Purpose  : Take input from Users

import wget
import os
import tarfile
import shutil
import paramiko
import logging
import time
import os.path

print('')
print("                 Welcome to Automate World")
print("")
print("               It’s automation, not automagic")
print('')
print("     -----let’s get started with a beautiful smile-----")
print('')
buil = input("Don't shy, Give me Version number what you want to download:  ")
buil1 = input("Enter the Build number. Share it fast, we dont have much time: ")
ver = input("Share your OS Release Details in number format: ")
ui_prs = input("Enter your OLD 742 NFUI Port Which you want to kill before upgrade 742 UI:  ")
base = input("Requires upgrade with base url [(yes or no)]")
print('')
if base == 'yes':
    base_ur = input('enter the value what you want to of base_url :')
else:
    print('Now all upgrade will be without baseurl')


def glbver():
    print('')
    print("           Build is----"+buil+"."+"#B"+buil1+' '+"And ISO is--U"+ver)
    print("")

