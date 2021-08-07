import functions
import csv
import testlink
import json
import time
import sys

tls = testlink.TestlinkAPIClient('http://10.10.30.104/testlink/lib/api/xmlrpc/v1/xmlrpc.php', '8bf45c0d9ef497fac24dcf10ae8375c3')


def trimChar(value):
    value = value.replace('<p>','')
    value = value.replace('</p>\n','')
    value = value.replace('<strong>','')
    value = value.replace('</strong>','')
    value = value.replace('<em>','')
    value = value.replace('</em>','')
    value = value.replace('&nbsp;','')
    value = value.replace('\n','')
  #  value = value.replace('|','')
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
    value=  value.replace('||', '| ')
    return value



#Updating Results in CSV file
def resultUpdate(testcase,testplan,build):
    print("making queue of all test cases and starting test now...\n...................................................\n")
    failed_cases = []
    skipped_cases = []
    passed_cases = []
    timeout_cases = []
    incomplete_cases = []
    testcase_executed = []
    with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='@', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Testcase_Id','TC_Name','Query','Type_of_TC', 'Status', 'ActualResult','Current'])
        csvfile.flush()


    for i in testcase:
        a = tls.getTestCase(i)
        field1 = a[0]['steps'][0]['actions']
        field1 = trimChar(field1)
      #  print(field1)
        try:
            keyword = tls.listKeywordsForTC(i)
        except AttributeError:
            keyword = []
        if 'Negative' in keyword or 'negative' in keyword:
            Type_of_TC = 'Negative'
        else:
            Type_of_TC = 'Positive'

        testcase_id = a[0]['full_tc_external_id']
        testcase_name = a[0]['name']
        payload_path = functions.getpayload(i)
        if payload_path == None:
            status = ('null','b','payload_missing')
            skipped_cases.append(i)
            functions.raw_result(testcase_id,testcase_name,field1,Type_of_TC,'Not Run','Payload missing','-')
            print("..............................................")
        else:
            try:
                expected = functions.testlink_output(i,Type_of_TC,field1)
                print("Read the expected output for the test case...")
                print("Checking the response coming from nfdb...")
                print("Expected3:", str(expected))

                try:
                    if Type_of_TC == 'Positive':
                        status = functions.comparison(expected, payload_path)
                    else:
                        print("Negative test case")
                except:
                    print("Getting no resposnse from nfdb")
                    status = 'Timeout'

                try:
                    if Type_of_TC == 'Negative':
                        status = functions.Negativetestcase_comparision(expected, payload_path)
                    else:
                        print("Negative testcases")
                except Exception:
                    print("Getting no resposnse from nfdb")

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print("Getting no resposnse from nfdb")
                status = 'Timeout'
            except IndexError:
                # need to update something in this
                print('Steps are not complete in the test case..update..')
                status = 'Incomplete_TC'

        if status[1] == 'p':
            functions.updatetestcase(i, testplan, build, 'p', 'linux')
            ActualResult = 'Test case passed, hit are coming as expected and fields are matching as expected'
            functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Pass', ActualResult, status[0])
            passed_cases.append(i)

        elif status[1] == 'f':
            count = 0
            flag = True
            while count < 1:
                print("Again testing the test case")
                expected = functions.testlink_output(i, Type_of_TC, field1)
                status = functions.comparison(expected, payload_path)
                if status[0] == 'f':
                    wait = 0
                    while wait < 1:
                        time.sleep(1)
                        print('.')
                        wait += 1
                elif status[0] == 'p':
                    flag = False
                    break
                count += 1
            if flag:
                if status[2] == 'hits':
                    ActualResult = "Test case failed because hits are not matching expected hits was "+str(status[3])+" but hits coming are "+str(status[4])
                    functions.raw_result(testcase_id,testcase_name,field1,Type_of_TC, 'Fail', ActualResult,status[0])
                elif status[2] == 'value':
                    ActualResult = "Test case failed because value of field '"+str(status[5])+"' is not coming correct. It was expected to be '"+str(status[3])+"' but we are getting '"+str(status[4])+"'. Number of hits coming for this test case is "+str(status[6])+" which is same as expected."
                    functions.raw_result(testcase_id,testcase_name,field1,Type_of_TC, 'Fail', ActualResult,status[0])

                elif status[2] == 'field':
                    ActualResult = "Test case failed because '" + str(status[3]) + "' field is not present in the output. However number of hits coming is " + str(status[5]) + " which is same as expected."
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Fail', ActualResult,status[0])
                elif status[2] == '':
                    ActualResult = "Some key error exception occured, not able to send request to nfdb"
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Fail', ActualResult,status[0])
                elif status[2] == 'incomplete':
                    ActualResult = "Failed because test case is incomplete. Third step is not prestent. Verify it on testlink"
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Incomplete_TC', ActualResult,status[0])
                elif status[2] == 'parse':
                    ActualResult = "Getting parse exception. Something wrong with payload or syntax of the query got changed"
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Fail', ActualResult,status[0])
                elif status[2] == 'nullpointer':
                    ActualResult = "Getting null pointer exception"
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Fail', ActualResult,status[0])
                elif status[2] == 'fetch':
                    ActualResult = "No metrics found based on the graph/metric pattern."
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Fail', ActualResult,status[0])
                else:
                    ActualResult = "Testcase Passed after retesting"
                    functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Pass', ActualResult,status[0])
                    passed_cases.append(i)
                if status[2] == 'incomplete':
                    incomplete_cases.append(i)
                else:
                    failed_cases.append(i)
            else:
                ActualResult = "passed after retesting"
                functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Pass', ActualResult, status[0])
                passed_cases.append(i)
        elif status == 'Timeout':
            ActualResult = "Getting timeout for this test case. Check request payload and nfdb logs"
            functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Timeout', ActualResult, '90+sec')
            timeout_cases.append(i)
        elif status == 'Incomplete_TC':
            ActualResult = "Test case seems to be incomplete. Verify it on testlink"
            functions.raw_result(testcase_id, testcase_name, field1, Type_of_TC, 'Incomplete_TC', ActualResult, '-')
            incomplete_cases.append(i)
        testcase_executed.append(i)

    #    failed_tc_count = len(failed_cases)
    skipped_tc_count = len(skipped_cases)
    passed_tc_count = len(passed_cases)
    timeout_tc_count = len(timeout_cases)
    incomplete_tc_count = len(incomplete_cases)
    total_tc_executed = len(testcase_executed)
    failed_tc_count = total_tc_executed - passed_tc_count - skipped_tc_count - timeout_tc_count - incomplete_tc_count
    with open('ExecutedTC.txt', 'w') as f:
        f.write(json.dumps(testcase_executed))
    return total_tc_executed, passed_tc_count, timeout_tc_count, failed_tc_count, skipped_tc_count, incomplete_tc_count
