import os, signal


def process():
    name = input("Enter process Name: ")
    try:
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
            print(fields)
            '''
            pid = fields[0]
            print(pid)
            os.kill(int(pid), signal.SIGKILL)  '''

        print("Process Successfully terminated")
    except:
        print("Error Encountered while running script")


process()
