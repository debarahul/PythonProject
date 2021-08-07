import platform
import functions
import csv
import testlink
import time
import pandas
import json
import Result_update
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.mimeapplication import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

tls = testlink.TestlinkAPIClient('http://10.10.30.104/testlink/lib/api/xmlrpc/v1/xmlrpc.php','8bf45c0d9ef497fac24dcf10ae8375c3')
print("Welcome to automation Suit...")
result = (0,0,0,0,0)
parameters = []
projectid = functions.getprojects()
#To fetch test plan id
testplan = functions.getTestplans(projectid)
#to fetch build
build = functions.getbuilds(testplan)
#platform = functions.getplatform(testplan)
testsuitid = functions.getTestsuitid(projectid)
subtestsuitid = functions.getsubsuitid(testsuitid)
build_name = testplan + build
print(build_name)
choice ='6'
print("Extracting the testcases which needs to be executed...it might take few minutes...\n")
if choice == '1' or choice == 'Low Priority':
    testcase,ext_testcaseid = functions.gettestcaseImportance(testsuitid,'1')
elif choice == '2' or choice == 'Medium Priority':
    testcase,ext_testcaseid = functions.gettestcaseImportance(testsuitid,'2')
elif choice == '3' or choice == 'High Priority':
    testcase,ext_testcaseid = functions.gettestcaseImportance(testsuitid,'3')
elif choice == '4' or choice == 'Very Low Priority':
    testcase,ext_testcaseid = functions.gettestcase(testsuitid,'4')
elif choice == '5' or choice == 'Smoke':
    allcase = functions.gettestcase(testsuitid)
    testcase,ext_testcaseid = functions.getsmoketestcase(allcase)
elif choice == '6' or choice == 'all':
    testcase,ext_testcaseid = functions.gettestcase(subtestsuitid)
    #testcase,ext_testcaseid = functions.get_external_tc_from_file()   
    #testcase,ext_testcaseid = functions.gettestcase(testsuitid)
    #testcase = functions.gettestcase(testsuitid)
parameters.append(projectid)
parameters.append(testplan)
parameters.append(build)
parameters.append(testsuitid)
with open('testcase_id_1.txt','w') as f:
    f.write(json.dumps(testcase))
with open('build_parameters.txt', 'w') as f:
    f.write(json.dumps(parameters))
alltestcases = len(testcase)
print("Total Automated test cases :",alltestcases)
print(testcase)
#ask = input("dou u want to add test cases to test plan(y/n)\n",)
#if ask == "y":
#functions.add_test_cases_to_test_plan(ext_testcaseid,projectid,testplan)
    
#functions.assign_user_to_test_case(testplan,build,ext_testcaseid)

#test_case = functions.result_update_testlink(testcase,testplan,build,status)
#print('Summary')


result = Result_update.resultUpdate(testcase,testplan,build)
print(result)
with open('summary.csv', 'w', newline='', encoding='utf-8') as csvfile:
    filewriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Summary @','Count'])
    filewriter.writerow(['Total test case executed @',result[0]])
    filewriter.writerow(['Total test case passed @',result[1]])
    filewriter.writerow(['Total test case timed out @' ,result[2]])
    filewriter.writerow(['Total test case failed @',result[3]])
    filewriter.writerow(['Total test case skipped @',result[4]])
    filewriter.writerow(['Incomplete test case @',result[5]])
print("Total TC executed:",result[0])
print("Total TC Passed:",result[1])
print(result)
print("Total TC Timed out:",result[2])
print("Total TC failed:",result[3])
print("Total TC skipped:",result[4])
print('Incomplete test case:',result[5])

dataframe_1 = pandas.read_csv('result.csv', delimiter='@')
dataframe_2 = pandas.read_csv('summary.csv', delimiter='@')
x="report"
y=".xlsx"
a="-"
testplans="maxdocs"
File=x+a+testplans+y
#File=x+y
excel_writer = pandas.ExcelWriter(File, engine='xlsxwriter')
dataframe_2.to_excel(excel_writer,'Summary')
dataframe_1.to_excel(excel_writer,'TestCase Status')
excel_writer.save()
#send_mail=functions.send_mail()

