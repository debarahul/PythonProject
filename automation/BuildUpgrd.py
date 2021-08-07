import wget
import tarfile
import os
import shutil
import paramiko
import logging
import time

from cryptography.hazmat.primitives.serialization import ssh


def BuildUp():
    val = input("Enter NFDB Version number: ")
    print(val)
    val1 = input("Enter the Build number: ")
    print(val1)
    key = "nfdb742-"
    j = key + val + val1
    print(j)
    key1 = ".tar.gz"
    url = "http://10.20.0.82:8992/others/NETFOREST/" + key + val + val1 + key1
    print(url)
    filename = wget.download(url)
    print(filename)
    print("Build Download Successfully")
    t = tarfile.open(filename, 'r')
    p = t.extractall()
    print("build is succesfully untared")
    directory = "lookup"
    parent_dir = "/home/cavisson/work/debasish/singlenode" + j + "/config/"
    print(parent_dir)
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print("Directory '%s' created" % directory)
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/file.json',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/lookup/')
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/file1.json',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/lookup/')
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/kohls_prod_stores.json',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/lookup/')
    shutil.copy(
        '/home/cavisson/work/debasish/singlenode/automate_build/kohls_stores_overall_health_L0_summary_lookup.json',
        '/home/cavisson/work/debasish/singlenode' + j + '/config/lookup/')
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/nfdb.yml',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/')
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/jvm.options',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/')
    # shutil.copy('/home/cavisson/work/nfdb742/nfdb/auto_build/nfdb','/home/cavisson/work/nfdb742/nfdb/'+j+'/bin/')
    # shutil.copy('/home/cavisson/work/nfdb742/nfdb/auto_build/nfdb_as_service.sh','/home/cavisson/work/nfdb742/nfdb/'+j+'/nf-tools/Daemon_service/Ubuntu_16.04')
    shutil.copy('/home/cavisson/work/debasish/singlenode/automate_build/log4j2.properties',
                '/home/cavisson/work/debasish/singlenode' + j + '/config/')
    # shutil.copy('/home/cavisson/work/nfdb742/nfdb/auto_build/nfui_as_service.sh','/home/cavisson/work/nfdb742/nfdb/'+j+'/nf-tools/Daemon_service/Ubuntu_16.04')
    '''
    logging.debug("we are in method to create service the nfdb")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host="10.20.0.89"
    user="cavisson"
    pas="cavisson_nf2!"
    ssh.connect(hostname=host, username=user, password=pas)      '''
    j = key + val + val1
    time.sleep(5)
    print("We are going to stop the service and perform to download latest build")
    # cmd= 'cd '+'/home/cavisson/work/nfdb742/nfdb/nfdb742-4.5.0.38/nf-tools/Daemon_service/Ubuntu_16.04;service nfdb stop' +'/home/cavisson/work/nfdb742/nfdb/nfdb742-4.5.0.38/nf-tools/Daemon_service/Ubuntu_16.04;./nfdb_as_service.sh -f ./nfdb.template -u cavisson -p /home/cavisson/work/nfdb742/nfdb/'+j+' -j /home/cavisson/work/suraj/jdk-12/bin -install'
    cmd = 'cd ' + '/home/cavisson/work/debasish/singlenode' + j + '/bin;export JAVA_HOME=/home/cavisson/work/debasish/nfdb-7.4/jdk-12;export PATH=$JAVA_HOME/bin:$PATH;./nfdb -d'
    print(cmd)
    time.sleep(5)
    print("Now the Build Process Executed successfully")
    #    stdin, stdout, stderr = ssh.exec_command(cmd1)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)
    ssh.close()


BuildUp()

