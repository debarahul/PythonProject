# Name     : grep_kill_prcs.py
# Author   : Debasish
# Purpose  : For Kill running process before upgrade

import os, signal
import glb
import re



def process_kill(name):
    #name = input("Enter process Name: ")
    #print("---I am killing now the NFDB process before upgrade new version of NFDB---")
    print('')
    try:
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
            #print(fields)

            pid = fields[0]
            #print(pid)
            os.kill(int(pid), signal.SIGKILL)

        print('')
        print("---Process Successfully terminated---")
    except:
        print("Error Encountered while running script, Because there is no process running for same input")

#process_kill('<value>')


def old_nfui():
    print('')
    print("---I am killing now the NFUI process before upgrade new 742 UI---")
    print('')
    try:
        cmd = os.popen('netstat -natp|grep '+ glb.ui_prs)
        output = cmd.read()
        #print(output)
        res = output.split()
        pid = res[6]
        fnl = re.sub("/.*","", pid)
        print(fnl)
        os.kill(int(fnl), signal.SIGKILL)
    except Exception:
        print('')
        print("----Nothing in this process ID is running right now for NFUI----")
        print('')


#old_nfui()
