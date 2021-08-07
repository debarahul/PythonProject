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

from testlink import TestlinkAPIClient

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
        '''
        if field == 'type' and value == 'vis':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'vis'
            
        elif field == 'type' and value == 'avg_resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'avg_resptime'

        elif field == 'type' and value == 'host_id':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'host_id'    

        elif field == 'type' and value == 'resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'resptime'
            
        elif field == 'type' and value == 'jour':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'jour'

        elif field == 'type' and value == 'server':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'server'    
            
        elif field == 'type' and value == 'size':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'size'
            
        elif field == 'type' and value == 'sumhttp':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'sumhttp'    

        elif field == 'type' and value == 'ab':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'ab'
   
            
        elif field == 'type' and value == 'sum_a':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'sum_a'

        elif field == 'type' and value == 'add':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'add'    
            

        elif field == 'type' and value == 'ResponseTime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'ResponseTime'
            

        elif field == 'type' and value == 'max_resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'max_resptime'
        elif field == 'type' and value == 'newmin':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'newmin'     

        elif field == 'type' and value == 'min_resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'min_resptime'

        elif field == 'type' and value == 'count_resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'count_resptime'
            
        elif field == 'type' and value == 'sum_resptime':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'sum_resptime'

        elif field == 'type' and value == 'newsum':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'newsum'

        elif field == 'type' and value == 'httpmethod':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'httpmethod'     


        elif field == 'type' and value == 'newavg':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'newavg'

        elif field == 'type' and value == 'new':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)            
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'new'

            
        elif field == 'type' and value == 'makemv':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'makemv'


        elif field == 'type' and value == 'info':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'info'

        elif field == 'type' and value == 'summation':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'summation'

        elif field == 'type' and value == 'newmax':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'newmax'     


        elif field == 'type' and value == 'timeout':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'timeout'
            
        elif field == 'type' and value == 'hcode':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'hcode'

        elif field == 'type' and value == 'doccount':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'doccount'

        elif field == 'type' and value == 'min_b':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'min_b'      
            

        elif field == 'type' and value == 'c':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'c'
            
        elif field == 'type' and value =='RequestFormat':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'RequestFormat'
            

        elif field == 'type' and value == 'b':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'b'

        elif field == 'type' and value == 'newcount':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'newcount'

        elif field == 'type' and value == 'RespRange':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'RespRange'       

        elif field == 'type' and value == 'a':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'a'    

        elif field == 'type' and value == 'avg_bcd':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'avg_bcd'   
        elif field == 'type' and value == 'min_a':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'min_a'


        elif field == 'type' and value == 'sizeinbytes':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'sizeinbytes'

        elif field == 'type' and value == 'minimum':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'minimum'

        elif field == 'type' and value == 'maximum':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'maximum'

        elif field == 'type' and value == 'kfs':
             Testcase_field=a[0]['steps'][3]['actions']
             Testcase_field=trimChar(Testcase_field)
             field_value=a[0]['steps'][3]['expected_results']
             field_value=trimChar(field_value)
             return hits,Testcase_field,field_value,'kfs'
            
        else:
             return hits,field,value,'search'
    elif type_of_testcase == 'Negative':
    #if type_of_testcase == 'Negative':
        hits = a[0]['steps'][1]['expected_results']
        hits = trimChar(hits)
        print('field value===',hits)
        field = a[0]['steps'][2]['actions']
        field = trimChar(field)
        print('field value===',field)
        value = a[0]['steps'][2]['expected_results']
        value = trimChar(value)
    elif field == 'type' and value == 'exception':
        Testcase_field=a[0]['steps'][3]['actions']
        Testcase_field=trimChar(Testcase_field)
        field_value=a[0]['steps'][3]['expected_results']
        field_value=trimChar(field_value)
        return hits,Testcase_field,field_value,'exception'                      '''
    else:
        return hits,field,value
        #return hits
    response = a[0]['steps'][1]['expected_results']
    response = trimChar(response)
    print(response)
    return response



#check if payload file is present or not

def check_payload(testcaseid):
    a = tls.getTestCase(testcaseid)
    ext_testcaseid = a[0]['full_tc_external_id']
    try:
        path_list = sys.path
        current_path = path_list[0]
        current_path = current_path.replace('//', '/')
        #payload_path = '/home/cavisson/work' + '/' + 'paylo' +'/' + ext_testcaseid + '.json'
        payload_path = '/home/cavisson/work/suraj/UI/auto' + '/' + 'newpayload742' +'/' + ext_testcaseid + '.json'
        f = open(payload_path)
        f.close()
        return payload_path

    except FileNotFoundError:
        print("File is not present at path:'",payload_path,"' for test case'",ext_testcaseid,"'place payload at the path.." )
        print("skipping this test case\n")
        return None


def comparison(expected, payload_path):
    print("Hello there, executing in comparision method",expected)
    #Expected is a tuple of hits, field and value of field
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation/new_auto/query_added_payload.json'
    payload = open(payload_pa, 'r')
    pay=payload.read()
    #print(payload)
    time.sleep(5)
    # Send the query to the nfdb
    t1 = datetime.datetime.now()
    p = requests.post("http://10.20.0.98:7811/_msearch/job?pipetempindex=true&isSummaryIndex=false&MaxDocs=25000", data=pay, headers=head,  timeout=600)
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
            print("Expected Hits:", expected)
            print("Actual Hits:", hits)
            if str(hits) == str(expected):
            #if str(hits) > str(0):
                print("Value of the field is greater or same  as it is mentioned in test case")
                print("---- TESTCASE PASSED ----")
                return tdiff,'p', 'ok'
                '''
                type = expected[1]
                constrict = expected[2]
                type = type.casefold()
                constrict = constrict.casefold()
                if type == 'type' and constrict == 'vis':
                    print("VIS query - Matching only hits")
                    return tdiff,'p','VIS'
                else:
                    fields = []
                    try:
                        document = resp['hits']['hits'][0]['_source']
                        for keys in document:
                            fields.append(keys)
                        if expected[1] in fields:   # matching the keys in the document
                            print("field '"+expected[1]+"' is present in response and its value is '",document[expected[1]],"'")
                            if isinstance(document[expected[1]], str):
                                #print(type(expected[2]))
                                #print(type(document[expected[1]]))
                                #print("expected -"+expected[2]+ "document -"+ document[expected[1]])
                                if expected[2] == str(document[expected[1]]):
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff,'p','ok'
                                else:
                                    print("!!! TESTCASE FAILED !!!")
                                    print("Value of the field is different from the value mentioned in test case")
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
                                c = document[expected[1]]%1
                                if c > 0:
                                    if expected[2] == str(document[expected[1]]):
                                        print("Value of the field is same as it is mentioned in test case")
                                        print("---- TESTCASE PASSED ----")
                                        return tdiff,'p','ok'
                                    else:
                                        print("!!! TESTCASE FAILED !!!")
                                        print("Value of the field is different from the value mentioned in test case")
                                        print("Value expected was", expected[2], "value coming is", document[expected[1]])
                                        return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                                elif c == 0:
                                    if str(expected[2]) == str(int(document[expected[1]])) or str(expected[2]) == str(document[expected[1]]):
                                        print("Value of the field is same as it is mentioned in test case")
                                        print("---- TESTCASE PASSED ----")
                                        return tdiff,'p','ok'
                                    else:
                                        print("!!! TESTCASE FAILED--- !!!")
                                        print("Value of the field is different from the value mentioned in test case")
                                        print("Value expected was", expected[2], "value coming is", str(int(document[expected[1]])))
                                        return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                            elif isinstance(document[expected[1]], list):
                                new = ''
                                for i in document[expected[1]]:
                                    new = new + i +','
                                value = new[0:-1]
                                if value == expected[2]:
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff,'p', 'ok'                                
                                else:
                                    print("!!! TESTCASE FAILED !!!")
                                    print("Value of the field is different from the value mentioned in test case")
                                    print("Value expected was", expected[2], "value coming is", value)
                                    return tdiff,'f', 'value', expected[2], value, expected[1], hits, expected[1], hits
                            else:
                                return tdiff,'f', 'other type of value'
                        else:
                            print("!!! TESTCASE FAILED !!!")
                            print("Field mentioned in testlink is not coming in the response..")
                            return tdiff,'f', 'field', expected[1], 'Not Present', hits
                    except IndexError:
                        print("Test case is incomplete")
                        return tdiff,'f','incomplete'       '''
            else:
                print("!!! TESTCASE FAILED !!!")
                print("Number of hits coming is different from the hits mentioned in test case.")
                print("Hits expected:",expected)
                print("Hits coming: ",hits)
                return tdiff,'f', 'hits', expected, hits

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


def comparison1(expected, payload_path):
    print("Hello there, executing in comparision1 method")
    #Read the payload from the file
    #payload = open(payload_path, 'r')
    #pay=payload.read()
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation//new_auto/query_added_payload.json'
    payload = open(payload_pa, 'rt')
    pay=payload.read()
    time.sleep(2)
    # Send the query to the nfdb
    t1 = datetime.datetime.now()
    p = requests.post("http://10.20.0.67:7888/_msearch/job?pipetempindex=true&MaxDocs=30000", data=pay, headers=head,  timeout=600)
    t2 = datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000) 
    payload.close()
    print( tdiff)
    # checking the response of baseline nfdb
    baseline = json.loads(p.text)
    #print(baseline)
    #payload.close()
    for keys in baseline:
        try:
            array = baseline['responses']
            new = json.dumps(array[0])
            resp = json.loads(new)
            hits = resp['hits']['total']['value']
            
            if str(hits) >= expected[0]:
                type = expected[1]
                constrict = expected[2]
                type = type.casefold()
                constrict = constrict.casefold()
                if type == 'type' and constrict == 'vis':
                    print("VIS query - Matching only hits")
                    return tdiff,'p','VIS'
                else:
                    fields = []
                    try:
                        document = resp['hits']['hits'][0]['_source']
                        for keys in document:
                            fields.append(keys)
                        if expected[1] in fields:   # matching the keys in the document
                            print("field '"+expected[1]+"' is present in response and its value is '",document[expected[1]],"'")
                            if isinstance(document[expected[1]], str):
                                if expected[2] == document[expected[1]]:
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff,'p','ok'
                                else:
                                    print("!!! TESTCASE FAILED !!!")
                                    print("Value of the field is different from the value mentioned in test case")
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
                                c = document[expected[1]]%1
                                if c > 0:
                                    if expected[2] == str(document[expected[1]]):
                                        print("Value of the field is same as it is mentioned in test case")
                                        print("---- TESTCASE PASSED ----")
                                        return tdiff,'p','ok'
                                    else:
                                        print("!!! TESTCASE FAILED !!!")
                                        print("Value of the field is different from the value mentioned in test case")
                                        print("Value expected was", expected[2], "value coming is", document[expected[1]])
                                        return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                                elif c == 0:
                                    if expected[2] == str(document[expected[1]]):
                                        print("Value of the field is same as it is mentioned in test case")
                                        print("---- TESTCASE PASSED ----")
                                        return tdiff,'p','ok'
                                    else:
                                        print("!!! TESTCASE FAILED !!!")
                                        print("Value of the field is different from the value mentioned in test case")
                                        print("Value expected was", expected[2], "value coming is", document[expected[1]])
                                        return tdiff,'f', 'value', expected[2], document[expected[1]], expected[1], hits
                            elif isinstance(document[expected[1]], list):
                                new = ''
                                for i in document[expected[1]]:
                                    new = new + i +','
                                value = new[0:-1]
                                if value == expected[2]:
                                    print("Value of the field is same as it is mentioned in test case")
                                    print("---- TESTCASE PASSED ----")
                                    return tdiff,'p', 'ok'                                
                                else:
                                    print("!!! TESTCASE FAILED !!!")
                                    print("Value of the field is different from the value mentioned in test case")
                                    print("Value expected was", expected[2], "value coming is", value)
                                    return tdiff,'f', 'value', expected[2], value, expected[1], hits, expected[1], hits
                            else:
                                return tdiff,'f', 'other type of value'
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

            else:
                print(exp)
                return tdiff,'f', 'exception'            


def Negativetestcase_comparision(expected, payload_path):
    print("Hello there, executing in negative_comparision method")
    #payload=open(payload_path,'r')
    #pay=payload.read()
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation/new_auto/query_added_payload.json'
    payload = open(payload_pa, 'r')
    pay=payload.read()
    t1=datetime.datetime.now()
    response=requests.get("http://10.20.0.98:7811/_msearch/job?pipetempindex=true&MaxDocs=25000", data=pay, headers=head,  timeout=600)
    t2=datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000) 
    #payload.close()
    #payload.close()
    print( tdiff)
    a=json.loads(response.text)

    #print("response:",a)
    print(a['error']['root_cause'][0]['type'])
    id_field=(a['error']['root_cause'][0]['type'])
    print(id_field)

    print(expected[2])
    #print("hey")
    #print(id_field)
    if expected[2]==id_field:
        print("Value of the field mentioned in the testlink")
        print("---TESTCASE PASSED---")
        return tdiff,'p','ok'
    elif expected[2]!=id_field:
        print("Value of the field is not mentioned in the Testlink")
        print("---TESTCASE FAILED---")
        return tdiff,'f','ok'



def Negativetestcase1_comparision(expected,payload_path):
    print("Hello there, executing in Negativetestcase1_comp method")
    #payload=open(payload_path,'r')
    #pay=payload.read()
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation//new_auto/query_added_payload.json'
    payload = open(payload_pa, 'rt')
    pay=payload.read()
    t1=datetime.datetime.now()
    response=requests.get("http://10.20.0.67:7888/_msearch/job?pipetempindex=true&MaxDocs=30000", data=pay, headers=head,  timeout=600)
    t2=datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000) 
    payload.close()
    print( tdiff)
    a=json.loads(response.text)
    #print(a)
    print(a['responses'][0]['timed_out'])
    id_field=(a['responses'][0]['timed_out'])
    #print(id_field)
    #print(expected[2])
    #print(expected) 
    if str(expected[2])==str(id_field):
        print("Value of the field mentioned in the testlink")
        print("---TESTCASE PASSED---")
        return tdiff,'p','ok'
    elif str(expected[2])!=str(id_field):
        print("Value of the field is not mentioned in the Testlink")
        print("---TESTCASE FAILED---")
        return tdiff,'f','ok'


def vis_comparison(expected,payload_path):
    print("Hello there, executing in vis_comparision method")
    #payload = open(payload_path, 'r')
    #pay=payload.read()
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation//new_auto/query_added_payload.json'
    payload = open(payload_pa, 'rt')
    pay=payload.read()
    t1=datetime.datetime.now()
    response=requests.get("http://10.20.0.67:7888/_msearch/job?pipetempindex=true&MaxDocs=30000", data=pay, headers=head,  timeout=600)
    t2=datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000) 
    payload.close()
    print( tdiff)
    baseline = json.loads(response.text)
    total_hits=baseline['responses'][0]['hits']['total']['value']
    print(total_hits)
    if str(total_hits) >= str(expected[0]):
         print("hits matching")
         print("Value of the field mentioned in the testlink")
         print("---- TESTCASE PASSED ----")
         return tdiff,'p','ok'
    else:
         print("Hits not matching..")
         print("---TESTCASE FAILED---")
         return tdiff,'f','hits',expected[0],total_hits    



def get_comparision(expected,payload_path):
    print("Hello there, executing in get_comparision method")
    #payload=open(payload_path,'r')
    #pay=payload.read()
    payload_pa = '/home/cavisson/work/debasish/nfdb742/automation//new_auto/query_added_payload.json'
    payload = open(payload_pa, 'rt')
    pay=payload.read()
    t1=datetime.datetime.now()
    response=requests.get("http://10.20.0.67:7888/_msearch/job?pipetempindex=true&MaxDocs=30000", data=pay, headers=head,  timeout=600)
    t2=datetime.datetime.now()
    t3 = (t2 - t1)
    tdiff=int(t3.total_seconds() * 1000) 
    payload.close()
    print( tdiff)
    a=json.loads(response.text)
    total_hits=a['responses'][0]['hits']['total']['value']
    if str(total_hits) >= str(expected[0]):
        #print(total_hits)
        questions_access=a['responses'][0]['hits']['hits']
        last_index = len(questions_access) - 1
        for questions_data in questions_access:
            last_index = last_index - 1
            #print(last_index)
            if str(expected[3]) == "resptime":
                id_field=questions_data['_source']['resptime']
  
            elif str(expected[3]) =="RequestFormat":
                id_field=questions_data['_source']['RequestFormat']
            elif str(expected[3]) =="minimum":
                id_field=questions_data['_source']['minimum']
            elif str(expected[3]) =="maximum":
                id_field=questions_data['_source']['maximum']

            elif str(expected[3]) == "a":
                id_field=questions_data['_source']['a']
            elif str(expected[3]) == "RespRange":
                id_field=questions_data['_source']['RespRange']    
            elif str(expected[3]) == "doccount":
                id_field=questions_data['source']['doc_count']
            elif str(expected[3]) =="b":
                id_field=questions_data['_source']['b']
                print(id_field)
            elif str(expected[3]) =="httpmethod":
                id_field=questions_data['_source']['httpmethod']
                print(id_field)
                
            elif str(expected[3]) =="summation":
                id_field=questions_data['_source']['summation']
            elif str(expected[3]) =="c":
                id_field=questions_data['_source']['c']
            elif str(expected[3]) =="info":
                id_field=questions_data['_source']['type']      
            elif str(expected[3]) =="makemv":
                id_field=questions_data['_source']['users']
                #print(id_field)
            elif str(expected[3]) =="avg_resptime":
                id_field=questions_data['_source']['avg_resptime']
            elif str(expected[3]) =="jour":
                id_field=questions_data['_source']['jour']
            elif str(expected[3]) =="size":
                id_field=questions_data['_source']['size']
            elif str(expected[3]) =="ab":
                id_field=questions_data['_source']['ab']
            elif str(expected[3]) =="sum_a":
                id_field=questions_data['_source']['sum_a']
            elif str(expected[3]) =="max_resptime":
                id_field=questions_data['_source']['max_resptime']
            elif str(expected[3]) =="avg_resptime":
                id_field=questions_data['_source']['avg_resptime']
            elif str(expected[3]) =="min_resptime":
                id_field=questions_data['_source']['min_resptime']
            elif str(expected[3]) =="count_resptime":
                id_field=questions_data['_source']['count_resptime']    
            elif str(expected[3]) =="sum_resptime":
                id_field=questions_data['_source']['sum_resptime']
            elif str(expected[3]) =="newmax":
                id_field=questions_data['_source']['newmax']
            elif str(expected[3]) =="newmin":
                id_field=questions_data['_source']['newmin']
            elif str(expected[3]) =="sumhttp":
                id_field=questions_data['_source']['sum_httpstatuscode']
            elif str(expected[3]) =="add":
                id_field=questions_data['_source']['add']
            elif str(expected[3]) =="newcount":
                id_field=questions_data['_source']['newcount']     
            elif str(expected[3]) =="new_min":
                id_field=questions_data['_source']['new_min']
            elif str(expected[3]) =="ResponseTime":
                id_field=questions_data['_source']['ResponseTime']    
            elif str(expected[3]) =="newsum":
                id_field=questions_data['_source']['newsum']
            elif str(expected[3]) =="newavg":
                id_field=questions_data['_source']['newavg']
            elif str(expected[3]) =="new":
                id_field=questions_data['_source']['new']
            elif str(expected[3]) =="hcode":
                id_field=questions_data['_source']['hcode']    
            elif str(expected[3]) =="avg_bcd":
                id_field=questions_data['_source']['avg_bcd']
            elif str(expected[3]) =="min_a":
                id_field=questions_data['_source']['min_a']
            elif str(expected[3]) =="min_b":
                id_field=question_data['_source']['min_b']
            elif str(expected[3]) =="sizeinbytes":
                id_field=questions_data['_source']['sizeinbytes']
            elif str(expected[3]) =="kfs":
                id_field=questions_data['_source']['kfs']
            elif str(expected[3]) =="host_id":
                id_field=questions_data['_source']['host_id']                          
            else:
                id_field=questions_data['_source']['add']
            #print(id_field)
            if str(expected[2])== str(id_field):
                print("Value of the field mentioned in the testlink")
                print("---TESTCASE PASSED---")
                return tdiff,'p','ok',id_field
            elif str(expected[2])!= str(id_field) and last_index == 0:
                print("Value of the field mentioned in the testlink")
                print("---TESTCASE FAILED---")
                return tdiff,'f','ok','other type of value'   
        
    else:
        print("Hits not matching")
        print("Testcase failed")
        return tdiff,'f',expected[0]


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

def add_test_cases_to_test_plan(ext_testcaseid,projectid,testplan):
       for i in ext_testcaseid:
            tc_version = 1
            response = tls.addTestCaseToTestPlan(projectid, testplan, i,tc_version )
            print("addTestCaseToTestPlan", response)



def assign_user_to_test_case(testplan,build,ext_testcaseid):
      for i in ext_testcaseid:
            response = tls.assignTestCaseExecutionTask('debasish.nayak', testplan, i, buildname=build)
            #newResult = tls.reportTCResult(i, testplan, build, 'p', 'first try')
            print("assignTestCaseExecutionTask", response)
          


def updatetestcase(testcase,testplan,build,status,platform):
    print("function called success")
    tls.reportTCResult(testcase, testplan, build, status,'',platformname=platform,user='debasish.nayak')
    print("Updated succesfully")
            
            
            

#Asssigning test case to user
def assigntestcase(testplan, testcase, build, platform):
    b = tls.getTestCase(testcaseid)
    testcase_externalid = b[0]['full_tc_external_id']
    a = tls.getTestCaseAssignedTester(testplan,testcase_externalid,buildname=build,platformname=platform,devKey='8bf45c0d9ef497fac24dcf10ae8375c3')
    print(a)


#Function to compare hits field and expected value .



#Function to compare hits field and expected value .

                
    
#extract builds for the test plan
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


#extract automated test cases with importance
def gettestcaseImportance(testsuitid, importance):
    d = tls.getTestCasesForTestSuite(testsuitid,'true','full')
    print(d)
    testcaseapi = []
    ext_testcaseid = []
    for n in d:
        if n['execution_type'] == '3' and n['importance'] == importance:
            testcaseapi.append(n['id'])
            ext_testcaseid.append(n['external_id'])
    return testcaseapi,ext_testcaseid

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

#extracting testcase having smoke keyword
def getsmoketestcase(alltestcase):
    testcaseapi = []
    for i in alltestcase:
        try:
            keyword = tls.listKeywordsForTC(i)
        except AttributeError:
            keyword = []
        if 'Smoke' in keyword:
            testcaseapi.append(i)
    return testcaseapi
            

#Extract all the test suits
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



#To create the testcase on testlink functions

def createTestCase(self, *argsPositional, **argsOptional):
  #  positional args: testcasename, testsuiteid, testprojectid, authorlogin,summary
  #  optional args : steps, preconditions, importance, executiontype, order,internalid, checkduplicatedname, actiononduplicatedname,status, estimatedexecduration
    if self.stepsList:
        if 'steps' in argsOptional:
            raise TLArgError('confusing createTestCase arguments - '+'.stepsList and method args define steps')
        argsOptional['steps'] = self.stepsList
        self.stepsList = []
        return super(TestlinkAPIClient, self).createTestCase(*argsPositional,**argsOptional)

        

#Extract the platform of the test plan
def getplatform(testplan):
    a = tls.getTestPlanPlatforms(testplan)
    return a[0]['name']



def updatetestcase(testcase,testplan,build,status,platform):
    tls.reportTCResult(testcase, testplan, build, status,'',platformname=platform,user='debasish.nayak')
    

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

#Remove the testcase keyword from testcase        
def removetestcaseKeywords(testsuitid, keywords):
    details_tc = tls.getTestCasesForTestSuite('448617','deep','details')
    print(details_tc)
    size_of_details_tc = len(details_tc)
    for i in range(0,size_of_details_tc):
        testcaseexternalid = details_tc[i]['external_id']
        print(testcaseexternalid)
        tls.removeTestCaseKeywords({testcaseexternalid:'4.2.1 '})
       # print("removed")


#TODO getTestCaseID and addTestCaseKeyword
def addtestcaseKeywords(testsuitid,keys):
    details_tc = tls.getTestCasesForTestSuite('448617','deep','details')
    size_of_details_tc = len(details_tc)
    for i in range(0,size_of_details_tc):
        tls.addTestCaseKeywords({details_tc[i]['external_id']: ['Automation verified suit-1']})
        print ("Done for", details_tc[i]['external_id'])
        
#To check the performance of testcase 
def calculatePerformance():
    list=[]
    CurrentColumn=[]
    df=pd.read_excel("report.xlsx","TestCase Status")
    Current_Resptime=(df['Current(ms)']).values.tolist()
    print(Current_Resptime)
    df1=pd.read_excel("Baseline.xlsx","TestCase Status")            
    Baseline_Resptime=(df1['Baseline(ms)']).values.tolist()
    print(Baseline_Resptime)
    df3=pd.read_excel("report.xlsx","Summary")
    print(df3)
    i=0
    count=0
    for (a,b) in zip(Current_Resptime,Baseline_Resptime):
        result=((a-b)/b)*100
        print(result)
        result = round(result,2)
        print(result)
        list.append((result))
        i=i+1   
    st = []
    for i in list:
       if i>=25:
           st.append("Fail")
           count=count+1
       else:
           st.append("Pass")
    print(st)
    print(count)
    for j in Current_Resptime:
        print(j)
        CurrentColumn.append(int(j))   
    Status3=pd.DataFrame({'Current(ms)':CurrentColumn})
    print(Status3)
    Status2=pd.DataFrame({'Perf_Status':st})
    print(Status2)
    df=pd.DataFrame({'Change%((Current-Baseline)/Baseline)*100)':list})
    x=[df1,Status3,df,Status2]
    data=pd.concat(x,axis=1)
    print(data)
    new_row = {'Summary':'Fail Testcase Due to Query_Perf','Count':count}
    df3 = df3.append(new_row, ignore_index=True)
    excel_writer = pandas.ExcelWriter('report.xlsx', engine='xlsxwriter')
    df3.to_excel(excel_writer,sheet_name='Summary')
    data.to_excel(excel_writer,sheet_name='TestCase Status')
    excel_writer.save()


#Function For Comparision of two Report

def Reportcomparison():
    df=pd.read_excel("report.xlsx","TestCase Status")
    df2=pd.read_excel("report.xlsx","Summary")
    print(df2)
    Response_time=(df['Status']).values.tolist()
  #  print(Response_time)
    Response_time1=(df['TestCase_Id']).values.tolist()
    file = {}
    for n in Response_time1:
        for e in Response_time:
            file[n]=e
            Response_time.remove(e)
            break
    print(file)
    df1=pd.read_excel("report1.xlsx","TestCase Status")
    df3=pd.read_excel("report1.xlsx","Summary")
    print(df3)
    time=(df1['Status']).values.tolist()
    time1=(df1['TestCase_Id']).values.tolist()
    file1 = {}
    for i in time1:
        for j in time:
            file1[i]=j
            time.remove(j)
            break
    print(file1)
    st=[]
    SPass=0
    SFail=0
    STimeout=0
    count=0
    for i in Response_time1:
        if file1[i]=='Pass' and file[i]=='Pass':
            st.append('Testcase Passed in Both 5.4 Build And 7.4')
            SPass=SPass+1
        elif file1[i]=='Not Run' and file[i]=='Not Run':
            st.append('Testcase Payload are missing')
        elif file1[i]=='Pass' and file[i]=='Not Run':
            st.append('Testcase Pass in Previous Build but Payload missing in Current Build')
        elif file1[i]=='Fail' and file[i]=='Not Run':
            st.append('Testcase Fail in Previous Build but Payload missing in Current Build')
        elif file1[i]=='Not Run' and file[i]=='Pass':
            st.append('Testcase Payload missing in Previous Build but Pass in Current Build')
              
        elif file1[i]=='Fail' and file[i]=='Fail':
            st.append('Testcase Failed in Both 5.4 Build And 7.4')
            SFail=SFail+1
        elif file1[i]=='Pass' and  file[i]=='Fail':
            st.append('Testcase Passed in 5.4 But Failed in 7.4')
            SFail=SFail+1
        elif file1[i]=='Fail' and file[i]=='Pass':
            st.append('Testcase Failed in 5.4 But Passed in 7.4')
            SPass=SPass+1
        elif file[i]=='Timeout' and file[i]=='Timeout':
            st.append('Testcase timeout in both 5.4 And 7.4')
            STimeout=STimeout+1
        elif file1[i]=='Pass' and file[i]=='Timeout':
            st.append('Testcase Passed in 5.4 but Timeout in 7.4')
            STimeout=STimeout+1
        elif file1[i]=='Fail' and file[i]=='Timeout':
            st.append('Testcase Fail in 5.4 but Timeout in 7.4')
            STimeout=STimeout+1
        elif file1[i]=='Timeout' and file[i]=='Pass':
            st.append('Testcase timeout in 5.4 but Passed in 7.4')
            SPass=SPass+1            
        elif file1[i]=='Timeout' and file[i]=='Fail':
            count=count+1
            st.append('Testcase Timeout in 5.4 But Fail in 7.4')
            SFail=SFail+1            
        else:
            st.append('Pass')
    print(st)
    print(SPass)
    print(SFail)
    print(STimeout)
    Status2=pd.DataFrame({'ComParison Report Previous Build Status':st})
    x=[df,df1,Status2]
    data=pd.concat(x,axis=1)
    Status=pd.DataFrame({'Previous Build Testcase count'})
    y=[df2,df3,Status]
    Datasummary=pd.concat(y,axis=1)
    excel_writer = pandas.ExcelWriter('report1.xlsx', engine='xlsxwriter')
    Datasummary.to_excel(excel_writer,'Summary')
    data.to_excel(excel_writer,sheet_name='TestCase Status')  
    excel_writer.save()

    
#Function for mail sending report

#email_user='gauravsinghspn111@gmail.com'
#email_send='gauravsinghspn121@gmail.com'


def send_mail():
    email_user='gaurav.singh@cavisson.com'
    email_send='dl-qa-nf@cavisson.com','sandeep.gupta@cavisson.com'
    email_send1='dl-dev-nf@cavisson.com'

    df=pd.read_excel("report.xlsx","Summary")
    print(df)
    X= df["Count"]
  #  print(X)
    print(X[0])
    message=EmailMessage()
    message['subject']="NFDB AUTOMATION REPORT"
    message['from']=email_user
    message['To']=email_send
    message['cc']=email_send1
    message.set_content('NFDB automation report')
    message.add_alternative("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
     <meta charset="UTF-8">
     <center>
     <title>NFDB automation suite Report</title>
     </head>
     <body>
     <h1> NFDB Automation Report </h1>
     <h1> NFDB BUILD  (4.3.0.93) <h1>
     <table border="5" width="400" height="200">
     <tr><th>Total TestcaseExecuted</th><th>{X[0]}</th></tr>
     <tr><th>Total TestcasePassed</th><th>{X[1]}</th></tr>
     <tr><th>Total Testcasefailed</th><th>{X[2]}</th></tr>
     <tr><th>Total Testcasetimedout</th><th>{X[3]}</th></tr>
     <tr><th>Total Testcaseskipped</th><th>{X[4]}</th></tr>
     <tr><th>Total TestcaseIncomplete</th><th>{X[5]}</th></tr>
      <table border="5" width="400" height="200">
     </table>
      <h3 style="font-family:Arial">NFDB automation report</h3>
      <h5 style="font-family:Arial">NetForest-QA(Extn:3310,3307)</h5>
      <h5 style="font-family:Arial">Cavisson System inc.</h5>
      <h5 style="font-family:Arial">E-84 Sector -63 Noida</h5>
      <button style="background-color:#df0040"></button>
     </body>
     </html>
     """.format(X=X),subtype='html')
 #  message.attach(MIMEText(message.set_content,'plain'))
    part = MIMEText('DOCTYPE html', 'DOCTYPE html')
   # fileattachment=MIMEApplication(filename,_subtype="filename")
    filename='report.xlsx'
    attachment=open(filename,'rb')
    part=MIMEBase('applications','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment;filename="+ filename)
    message.attach(part)
    text=message.as_string()                                
    server=smtplib.SMTP('smtp.gmail.com',587)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_user,'gauravsingh123')
    os.system("thunderbird -compose ',subject='subject',body='body',attachment='/path/to/file'") 
    server.send_message(message)
    print("Email sent successfully")

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

