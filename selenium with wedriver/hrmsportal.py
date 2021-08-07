from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


browser = webdriver.Chrome('chromedriver')
browser.get('http://10.10.20.24/SavvyHRMS/LoginPage.aspx')
print(browser.title)
browser.find_element_by_xpath('//*[@id="txtUserName"]').send_keys('CSA10221')
browser.find_element_by_xpath(
'//*[@id="txtPassword"]').send_keys('jeet8984@cavisson') # enter password in this field
browser.find_element_by_id(
'btnlogin').click()
print(browser.title)
time.sleep(7)
try:
    date = '15 01 2021'
    timefrom = '09:30 AM'
    timeTo = '08:25 PM'
    browser.get('http://10.10.20.24/SavvyHRMS/SelfService/OnDutyRequest.aspx')
    time.sleep(5)
    browser.find_element_by_xpath(
    '//*[@id="ODTab"]/div[1]/ul/li[2]').click()
    time.sleep(5)
    browser.find_element_by_xpath(
    '//*[@id="inputtxtODFromDate"]').send_keys(date)

    time.sleep(1)
    browser.find_element_by_xpath(
    '//*[@id="inputtxtODToDate"]').send_keys(date)

    browser.find_element_by_xpath(
    '//*[@id="inputtxtFromTime"]').send_keys(timefrom)

    browser.find_element_by_xpath(
    '//*[@id="inputtxtToTime"]').send_keys(timeTo)
    browser.find_element_by_id('dropdownlistContentddlODType').click()

    time.sleep(2)
    browser.find_element_by_xpath(
    '//*[@id="listitem3innerListBoxddlODType"]/span').click()

    browser.find_element_by_xpath(
    '//*[@id="txtReason"]').send_keys('Due to COVID 19')
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="btnRequest"]').click()
    print("OD Request Successfull")
except:
 print("OD Request NOT Successfull SOME ERROR")
finally:
 browser.quit()

# try:
# element = WebDriverWait(browser, 10).until(
# EC.presence_of_element_located(
# (By.LINK_TEXT, "http://10.10.20.24/SavvyHRMS/EmployeeDashboard.aspx"))
# )
# finally:
# # browser.quit()

# date = input("Date Format -- DD/MM/YYYY--- 04 01 2021 ")
# timefrom = input("Time Format -- HH/MM--- 09:29 AM ")
# timeTo = input("Time Format -- HH/MM--- 07:45 PM ")
