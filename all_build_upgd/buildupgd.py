# Name     : buildupgd.py
# Author   : Debasish
# Purpose  : This is the main file of suite

import wget
import os
import tarfile
import shutil
import paramiko
import logging
import time
import os.path
import thrdprty_and_nstrm
import nfdb_ui_and_nodesrv
import glb
import grep_kill_prcs


glbl_ver = glb.glbver()

print('')
print("---I am killing now the NFDB process before upgrade new version of NFDB---")
prs_kill_db = grep_kill_prcs.process_kill('Des.path.home=/home/cavisson/work/debasish/nfdb742/mltesting/')
db_upded = nfdb_ui_and_nodesrv.Nfdb_BuildUpd()

print('')
print('---I am killing now the nodeserver process before upgrade new version of Nodeserver---')
prs_kill_nodeserv = grep_kill_prcs.process_kill('app.js')
node_serv_upd = nfdb_ui_and_nodesrv.node_serv_upd()
prs_kill_ui = grep_kill_prcs.old_nfui()

try:
    ui_upded = nfdb_ui_and_nodesrv.Nfui_upd()
except Exception:
    print('')
    print('The 742-NFUI build you want to download is not available on bildub, else you have entered wrong input')
    print('')

try:
    thrd_and_netstrm = thrdprty_and_nstrm.Buildup()
except Exception:
    print('')
    print('The thirdparty and nestrom  build you want to download is not available on bildub, else you have entered wrong input')
    print('')

tomcat_restrt = thrdprty_and_nstrm.Tomcat()

print('')
print("")
print("   Thanku Have a Good Day. I know you can do it,jst beliave in yourself")
print('')

