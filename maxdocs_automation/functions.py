import testlink
import re
import array
import requests
import time
import json
import sys
import time
import csv
import datetime
import os
import smtplib
import pandas as pd
import xlsxwriter
import pandas
import csv
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.mimeapplication import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders


tls = testlink.TestlinkAPIClient('http://10.10.30.104/testlink/lib/api/xmlrpc/v1/xmlrpc.php','8bf45c0d9ef497fac24dcf10ae8375c3')
head = {'Content-type': 'application/json', 'Accept': 'application/json'}

#triming charcters

def trimChar(value):
    value = value.replace('<p>','')
    value = value.replace('</p>\n','')
    value = value.replace('<strong>','')
    value = value.replace('</strong>','')
    value = value.replace('<em>','')
    value = value.replace('</em>','')
    value = value.replace('&nbsp;','')
    value = value.replace('\n','')
    value = value.replace('<br />','')
    value = value.replace('</span>','')
    value = value.replace('&#39;','\'')
    value = value.replace('<span style="color:#2980b9">','')
    value = value.replace('</span>', '')
    value = value.replace(r'^"|"$', '')
    value = value.replace("^\"|\"$", "")
    value = value.replace(r'^"|"$', '')
    value = value.replace('quot', "")
    value = value.replace(';', "")
    value = value.replace('&', '"')
    value = value.replace('&', "")
    value = value.replace('||', '| ')
    value = value.replace('\"lt','<')
    value = value.replace('\"gt','>')
    value = value.replace('"','\\"')
    value = value.replace('\-','\\\-')
    value = value.replace('\:','\\\:')
    value = value.replace('\.','\\\.')
    value = value.replace('\_','\\\_')
    value = value.replace('\[','\\\[')
    value = value.replace('\]','\\\]')
    value = value.replace('\,','\\\,')


    return value


#function to extract the hits,field name and its value from Testlink
def testlink_output(test_case,type_of_testcase,field1):
    a = tls.getTestCase(test_case)
    ext_testcaseid = a[0]['full_tc_external_id']
    print("Executing Test case :",ext_testcaseid)
    field1 = a[0]['steps'][0]['actions']
    field1 = trimChar(field1)
    if type_of_testcase == 'Positive':
        hits = a[0]['steps'][1]['expected_results']
        #print('before triming hits',hits)
        hits = trimChar(hits)
        #print('after triming hits',hits)
        field = a[0]['steps'][2]['actions']
        field = trimChar(field)
        #print('field value',field)
        value = a[0]['steps'][2]['expected_results']
        value = trimChar(value)
        #print('field value===',value)
    elif type_of_testcase == 'Negative':
        hits = a[0]['steps'][1]['expected_results']
        hits = trimChar(hits)
        field = a[0]['steps'][2]['actions']
        field = trimChar(field)
        value = a[0]['steps'][2]['expected_results']
        value = trimChar(value)
    if field == 'type' and value == 'exception':
        Testcase_field = a[0]['steps'][3]['actions']
        Testcase_field = trimChar(Testcase_field)
        field_value = a[0]['steps'][3]['expected_results']
        field_value = trimChar(field_value)
        return hits, Testcase_field, field_value, 'exception'
    else:
        return hits, field, value
        #return hits
    response = a[0]['steps'][1]['expected_results']
    response = trimChar(response)
    #print(response)
    return response


def comparison(expected, payload_path):
    print("Hello there, executing in comparision method",expected)
    #Expected is a tuple of hits, field and value of field
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation/pratice/test/query_added_payload.json'
    payload = open(payload_pa, 'r')
    pay=payload.read()
    print(pay)
    time.sleep(5)
    # Send the query to the nfdb
    t1 = datetime.datetime.now()
    p = requests.post("http://10.20.0.98:7221/_msearch/job?pipetempindex=true&isSummaryIndex=false&MaxDocs=25000", data=pay, headers=head,  timeout=600)
    #p = requests.post("http://10.20.0.99:7118/_msearch/job?pipetempindex=true&isSummaryIndex=false", data=pay, headers=head,  timeout=600)
    t2 = datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000)
    print( tdiff)
    #payload.close()
    # checking the response of baseline nfdb
    baseline = json.loads(p.text)
    #payload.close()
    for keys in baseline:
        try:
            array = baseline['responses']
            new = json.dumps(array[0])
            resp = json.loads(new)
            hits = resp['hits']['total']['value']
            #if str(hits) > str(0):
            if str(hits) == expected[0]:
                constrict = expected[2]
                type = expected[1]
                type = type.casefold()
                constrict = constrict.casefold()
                fields = []

                try:
                    document = resp['hits']['hits'][0]['_source']
                    for keys in document:
                        fields.append(keys)
                    if expected[1] in fields:
                        print("field '"+expected[1]+"' is present in response and its value is '",document[expected[1]],"'")
                        if isinstance(document[expected[1]], str):
                            if expected[2] == str(document[expected[1]]):
                                print("Value of the field is same as it is mentioned in test case")
                                print("---- TESTCASE PASSED ----")
                                return tdiff,'p','ok'
                            else:
                                print("!!! TESTCASE FAILED !!!")
                                print("Number of hits coming is different from the hits mentioned in test case.")
                                print("Value expected :", expected[2])
                                print("Value coming :", document[expected[1]])
                                return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                        elif isinstance(document[expected[1]], int):
                            if expected[2] == str(document[expected[1]]):
                                print("Value of the field is same as it is mentioned in test case")
                                print("---- TESTCASE PASSED ----")
                                return tdiff,'p','ok'
                            else:
                                print("!!! TESTCASE FAILED !!!")
                                print("Value of the field is different from the value mentioned in test case")
                                print("Value expected : ", expected[2])
                                print("Value coming : ", document[expected[1]])
                                return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                        elif isinstance(document[expected[1]], float):
                            c = document[expected[1]] % 1
                            if c > 0:
                                if expected[2] == str(document[expected[1]]):
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff, 'p', 'ok'
                                else:
                                    print("!!! TESTCASE FAILED !!!")
                                    print("Value of the field is different from the value mentioned in test case")
                                    print("Value expected was", expected[2], "value coming is", document[expected[1]])
                                    return tdiff, 'f', 'value', expected[2], document[expected[1]], expected[1], hits
                            elif c == 0:
                                if str(expected[2]) == str(int(document[expected[1]])) or str(expected[2]) == str(
                                        document[expected[1]]):
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff, 'p', 'ok'
                                else:
                                    print("!!! TESTCASE FAILED--- !!!")
                                    print("Value of the field is different from the value mentioned in test case")
                                    print("Value expected was", expected[2], "value coming is",
                                          str(int(document[expected[1]])))
                                    return tdiff, 'f', 'value', expected[2], document[expected[1]], expected[1], hits
                        elif isinstance(document[expected[1]], list):
                            new = ''
                            for i in document[expected[1]]:
                                new = new + i + ','
                            value = new[0:-1]
                            if value == expected[2]:
                                print("Value of the field is same as it is mentioned in test case")
                                print("---- TESTCASE PASSED ----")
                                return tdiff, 'p', 'ok'
                            else:
                                print("!!! TESTCASE FAILED !!!")
                                print("Value of the field is different from the value mentioned in test case")
                                print("Value expected was", expected[2], "value coming is", value)
                                return tdiff, 'f', 'value', expected[2], value, expected[1], hits, expected[1], hits
                        else:
                            return tdiff, 'f', 'other type of value'
                    else:
                        print("!!! TESTCASE FAILED !!!")
                        print("Field mentioned in testlink is not coming in the response..")
                        return tdiff,'f', 'field', expected[1], 'Not Present', hits
                except IndexError:
                    print("Test case is incomplete")
                    return tdiff,'f','incomplete'
            else:
                print("!!! TESTCASE FAILED !!!")
                print("Number of hits coming is different from the hits mentioned in test case.")
                print("Hits expected:",expected[0])
                print("Hits coming: ",hits)
                return tdiff,'f', 'hits', expected[0], hits

        except KeyError:
            print("!!! TESTCASE FAILED !!!")
            print(baseline)
            exp = baseline['error']
            if exp['root_cause'][0]['type'] == 'parse_exception':
                print('Something wrong with request payload')
                return tdiff,'f', 'parse'

            elif exp['root_cause'][0]['type'] == 'null_pointer_exception':
                print('Getting null pointer exception')
                return tdiff,'f', 'nullpointer'

            elif exp['root_cause'][0]['type'] == 'exception' and exp['root_cause'][0]['reason'] == 'No metrics found based on the graph/metric pattern.':
                print('No metrics found based on the graph/metric pattern.')
                return tdiff,'f', 'fetch'

            else:
                print(exp)
                return tdiff,'f', 'exception'

def Negativetestcase_comparision(expected,payload_path):
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation/pratice/test/query_added_payload.json'
    payload = open(payload_pa, 'r')
    pay=payload.read()
    print(pay)
    time.sleep(5)
    t1=datetime.datetime.now()
    response = requests.post("http://10.20.0.98:7221/_msearch/job?pipetempindex=true&isSummaryIndex=false&MaxDocs=25000", data=pay, headers=head,  timeout=600)
    t2=datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000)
    a=json.loads(response.text)
    print(a['error']['root_cause'][0]['type'])
    id_field=(a['error']['root_cause'][0]['type'])
    print(id_field)
    print(expected[2])
    if expected[2]==id_field:
        print("Value of the field mentioned in the testlink")
        print("---TESTCASE PASSED---")
        return tdiff,'p','ok'
    elif expected[2]!=id_field:
        print("Value of the field is not mentioned in the Testlink")
        print("---TESTCASE FAILED---")
        return tdiff,'f','ok'

#Select the test projects
def getprojects():
    a = tls.getProjects()
    flag=0
    while True:
        for i in a:
            print(i['name'])
        name = 'NetForest'

        for n in a:
            name = name.casefold()
            n['name'] = n['name'].casefold()
            if n['name'] == name:
                flag = flag + 1
                print("ID'S For GETPROJECT METHOD")
                print (n['id'])
                return n['id']
                return n['id']

        if flag == 0:
            print("Enter the project from the list\n")

def getbuilds(testplan):
    a = tls.getBuildsForTestPlan(testplan)
    flag = 0
    print("folling are the build present in the test plan")
    while  True:
        for n in a:
            print(" ",n['name'])
        build = 'B2'
        for n in a:
            if build == n['name']:
                flag = flag + 1
                print("ID'S For GETBUILD METHOD")
                print (n['id'])
                return n['name']
                return n['name']
        if flag ==0:
            print("Please select a build from the list")
        else:
            break


def updatetestcase(testcase,testplan,build,status,platform):
    print("function called success")
    tls.reportTCResult(testcase, testplan, build, status,'',platformname=platform,user='debasish.nayak')
    print("Updated succesfully")


#extract automated test case from the suit
def gettestcase(testsuitid):
    d = tls.getTestCasesForTestSuite(testsuitid,'true','full')
    testcaseapi = []
    ext_testcaseid = []
    for n in d:
        if n['execution_type'] == '1':
            testcaseapi.append(n['id'])
            ext_testcaseid.append(n['external_id'])
    return testcaseapi,ext_testcaseid



def getTestsuitid(projectid):
    a = tls.getFirstLevelTestSuitesForTestProject(projectid)
    flag = 0
    print("\nSelect a test suit for testing")
    while True:
        for n in a:
            print(" ",n['name'])
        testsuit ='NFDB/NFAgents-7.4.2 & New GUI'

        for n in a:
            testsuit = testsuit.casefold()
            n['name'] = n['name'].casefold()
            if testsuit == n['name']:
                flag = flag + 1

                return n['id']
        if flag == 0:
            print("Select any test suit from the list")
        else:
            break
#Function to get sub suit id
def getsubsuitid(testsuitid):
    b = tls.getTestSuitesForTestSuite(testsuitid)
    flag = 0
    print("\nSelect a test suit for testing")
    while True:
        for n in b:
            print(" ",b[n]['name'])
        #testsuit = input("Select test suit for testing\n",)
        testsuit = "maxdocstest"
        for n in b:
            testsuit = testsuit.casefold()
            b[n]['name'] = b[n]['name'].casefold()
            if testsuit == b[n]['name']:
                flag = flag + 1
                return b[n]['id']
        if flag == 0:
            print("Select any test suit from the list")
        else:
            break


#Extract test plans for the project
def getTestplans(projectid):
    a = tls.getProjectTestPlans(projectid)
    flag = 0
    print("\nThis project is having following test plan")
    while True:
        for n in a:
            print(" ",n['name'])
        testplan = '4.6.0'
        for n in a:
            if testplan == n['name']:
                print("ID'S For GETTESTPLANS METHOD")
                print (n['id'])
                return n['id']
                return n['id']
                flag = flag + 1
        if flag == 0:
            print("Please select a test plan from the list")
        else:
            break


#TODO run selected test cases
def get_external_tc_from_file():
     testcaseapi = []
     ext_testcaseid = []
     file = open("testcase_id_1.txt", 'r').read().splitlines()[0]
     testcaseapi = json.loads(file)
     #print(testcaseapi)
     return testcaseapi,ext_testcaseid

#TODO add,modify and create required query
def modQuery(value):
    # add escape character before double quote
    print(value  , "==============================================")
    #value = value.replace('"','\\"').replace('\-','\\\-').replace('\:','\\\:').replace('\.','\\\.').replace('\_','\\\_').replace('\[','\\\[').replace('\]','\\\]').replace('\,','\\\,').replace('\"lt','<')
    # remove unnecessary part from the query
    mod_query = re.sub("^.*query=", "", value)
    print(mod_query, "==============================================")
    #mod_query = re.sub("ms\"}","ms\"}\n", value)
    #print(mod_query)
    fin = open("payloadskeleton.json", "rt")
    fout = open("query_added_payload.json", "wt")
    for line in fin:
        fout.write(line.replace('<my_query>', mod_query))
    fin.close()
    fout.close()
    fout = open("query_added_payload.json", "a")
    fout.write('\n')
    fout.close()
    return fout

def getpayload(testid):
    a = tls.getTestCase(testid)
    query_field = a[0]['steps'][0]['actions']
    query_field_value = trimChar(query_field)
    query_mod = modQuery(query_field_value)
    return query_mod

#Raw_result
def raw_result(TC_id,TC_name,query,Type_of_TC,status,ActualResult,Current):
    with open('result.csv', 'a', newline='',encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='@', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([TC_id,TC_name,query,Type_of_TC,status,ActualResult,Current])
        csvfile.flush()

