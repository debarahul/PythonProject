import os
import subprocess
import time
import timeit
import datetime

'''
while True:
    x=int(input())
    y=input()
    os.system(y)
    time.sleep(x)   '''
'''
x=int(input("Enter Repetatin   "))
y=int(input("Enter time interval "))
z=int(input("Enter the ProcessID  "))  '''
process, repeat, time_in = input("Enter ProcessID, Repataton, Timeinterval(sec): ").split()
for r in range(0,int(repeat)):
    time_f=time.time()
    dump= "withmax_threaddump-" + str(time_f) + ".txt"
    thread_d= "jstack" + ' ' + process +' '+ ">>" +' '+ str(dump)
    print(thread_d)
    os.system(thread_d)
    time.sleep(int(time_in))
