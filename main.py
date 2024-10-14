import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


driver = None
isSuccess = False

id = ''
pw = ''
departures = '광주송정'
arrivals = '수서'
date = '20241010'
hour = '12'
headCount = '2'


def driverFindClickAbleToXpath(xpath):
    global driver

    element = WebDriverWait(driver, 300000).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    return element


def driverFindLocatedToXpath(xpath):
    global driver

    element = WebDriverWait(driver, 300000).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element

def driverFindIgnoredExceptionToXpath(xpath):
    global driver

    ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

    element = WebDriverWait(driver, 300000, ignored_exceptions = ignored_exceptions).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    return element

def login(id, pw):
    btn_Login = driverFindClickAbleToXpath('//*[@id="wrap"]/div[3]/div[1]/div/a[2]')
    btn_Login.click()

    txt_id = driverFindLocatedToXpath('//*[@id="srchDvNm01"]')
    txt_id.send_keys(id)

    txt_pw = driverFindLocatedToXpath('//*[@id="hmpgPwdCphd01"]')
    txt_pw.send_keys(pw)

    btn_LoginConfirm = driverFindClickAbleToXpath('//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input')
    btn_LoginConfirm.click()


def searchTrainList(departures, arrivals, date, hour, headCount):
    global driver

    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000')

    txt_Departures = driverFindLocatedToXpath('//*[@id="dptRsStnCdNm"]')
    txt_Arrivals = driverFindLocatedToXpath('//*[@id="arvRsStnCdNm"]')

    txt_Departures.clear()
    txt_Departures.send_keys(departures)

    txt_Arrivals.clear()
    txt_Arrivals.send_keys(arrivals)

    slt_date = Select(driverFindLocatedToXpath('//*[@id="dptDt"]'))
    slt_date.select_by_value(date)

    hour += '0000'

    slt_time = Select(driverFindLocatedToXpath('//*[@id="dptTm"]'))
    slt_time.select_by_value(hour)

    slt_HeadCount = Select(driverFindLocatedToXpath('//*[@id="psgInfoPerPrnb1"]'))
    slt_HeadCount.select_by_value(headCount)

    rdo_TrainKind = driverFindClickAbleToXpath('//*[@id="trnGpCd300"]')
    rdo_TrainKind.click()

    btn_Search = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    btn_Search.click()

def researchTrainList():
    #print('researchTrainList')
    btn_ReSearch = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    btn_ReSearch.send_keys(Keys.ENTER)

    # try:
    #     btn_ReSearch.click()
    # except selenium.common.exceptions.StaleElementRefrenceException:
    #     btn_ReSearch = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    #     btn_Research.click()
    div_TrainList = driverFindLocatedToXpath('//*[@id="result-form"]/fieldset/div[6]')
    #print('div_TrainList ----------------', div_TrainList)

driver = webdriver.Chrome()
driver.get("https://etk.srail.kr/main.do")


login(id, pw)
searchTrainList(departures, arrivals, date, hour, headCount)

while isSuccess == False:
    for i in range(1, 11):
        #print("i = ", i)
        try:
            td = driverFindLocatedToXpath(f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[7]')
            print('td', td)
            btn_reservations = td.find_elements(By.TAG_NAME, 'a')
            print('btn_reservations', btn_reservations)
        except NoSuchElementException:
            print("--------NoSuchElementException--------")
            td = None
            btn_reservations = None
            continue
        except StaleElementReferenceException:
            print("--------StaleElementReferenceException--------")
            td = None
            btn_reservations = None
            time.sleep(1.5)
            continue
        except:
            input()

        if(len(btn_reservations) > 1):
            btn_reservations[0].click()
            isSuccess = True
            print('isSuccess', isSuccess)
            break
    researchTrainList()
    time.sleep(1)
