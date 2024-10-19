import time
import pyautogui
import config
import pyperclip
import cv2
#from skimage.measure import compare_ssim
import numpy as np
import slack_sdk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime

driver = None
isSuccess = False
isDone = False

slack_client = slack_sdk.WebClient(token=config.SLACK_INFO.TOKEN)
refreshCnt = 0
windowCnt = 0
macro_Start_hour = 0
macro_Start_Date = datetime.now()

def driverFindClickAbleToXpath(xpath):
    global driver

    element = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    return element


def driverFindLocatedToXpath(xpath):
    global driver

    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element

def driverFindIgnoredExceptionToXpath(xpath):
    global driver

    ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

    element = WebDriverWait(driver, 100, ignored_exceptions = ignored_exceptions).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    return element

def login(srtInfo):
    btn_Login = driverFindClickAbleToXpath('//*[@id="wrap"]/div[3]/div[1]/div/a[2]')
    btn_Login.click()

    txt_id = driverFindLocatedToXpath('//*[@id="srchDvNm01"]')
    txt_id.send_keys(srtInfo.ID)

    txt_pw = driverFindLocatedToXpath('//*[@id="hmpgPwdCphd01"]')
    txt_pw.send_keys(srtInfo.PW)

    btn_LoginConfirm = driverFindClickAbleToXpath('//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input')
    btn_LoginConfirm.click()


def searchTrainList(srtInfo):
    global refreshCnt
    global driver
    print("searchTrainList")
    refreshCnt+=1

    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000')

    txt_Departures = driverFindLocatedToXpath('//*[@id="dptRsStnCdNm"]')
    txt_Arrivals = driverFindLocatedToXpath('//*[@id="arvRsStnCdNm"]')

    txt_Departures.clear()
    txt_Departures.send_keys(srtInfo.DEPARTURES)

    txt_Arrivals.clear()
    txt_Arrivals.send_keys(srtInfo.ARRIVALS)

    slt_date = Select(driverFindLocatedToXpath('//*[@id="dptDt"]'))
    slt_date.select_by_value(srtInfo.DATE)

    if(len(srtInfo.HOUR) == 2):
        srtInfo.HOUR += '0000'

    slt_time = Select(driverFindLocatedToXpath('//*[@id="dptTm"]'))
    slt_time.select_by_value(srtInfo.HOUR)

    slt_HeadCount = Select(driverFindLocatedToXpath('//*[@id="psgInfoPerPrnb1"]'))
    slt_HeadCount.select_by_value(srtInfo.HEAD_COUNT)

    rdo_TrainKind = driverFindClickAbleToXpath('//*[@id="trnGpCd300"]')
    rdo_TrainKind.click()

    btn_Search = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    btn_Search.click()

def researchTrainList():
    global refreshCnt
    refreshCnt+=1
    #print('researchTrainList')
    btn_ReSearch = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    btn_ReSearch.send_keys(Keys.ENTER)

    # try:
    #     btn_ReSearch.click()
    # except selenium.common.exceptions.StaleElementRefrenceException:
    #     btn_ReSearch = driverFindClickAbleToXpath('//*[@id="search_top_tag"]/input')
    #     btn_Research.click()

    #div_TrainList = driverFindLocatedToXpath('//*[@id="result-form"]/fieldset/div[6]')
    
    #print('div_TrainList ----------------', div_TrainList)



def reservationBankWire():
    # 미사용
    global driver

    btn_checkout = driverFindClickAbleToXpath('//*[@id="list-form"]/fieldset/div[11]/a[1]')
    btn_checkout.click()

    li_bankWire = driverFindClickAbleToXpath('//*[@id="chTab3"]')
    li_bankWire.click()

    li_smartPhoneTicketing = driverFindClickAbleToXpath('//*[@id="select-form"]/fieldset/div[11]/div[2]/ul/li[2]/a')
    li_smartPhoneTicketing.click()

    alert = driver.switch_to.alert
    alert.accept()

def reservation(secondPassengerName):
    global driver

    btn_checkout = driverFindClickAbleToXpath('//*[@id="list-form"]/fieldset/div[11]/a[1]')
    btn_checkout.click()

    li_easyPayment = driverFindClickAbleToXpath('//*[@id="chTab2"]')
    li_easyPayment.click()

    time.sleep(1)

    txt_secondPassenger = driverFindLocatedToXpath('//*[@id="select-form"]/fieldset/div[11]/div[5]/div[3]/table/tbody/tr[2]/td[8]/input[2]')
    txt_secondPassenger.send_keys(secondPassengerName)

    btn_callPayment = driverFindClickAbleToXpath('//*[@id="requestIssue2"]')
    btn_callPayment.click()

def naverLogin(naverInfo):
    global driver
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-2])
    print("naverLogin")

    input_id = driverFindLocatedToXpath('//*[@id="id"]')
    input_pw = driverFindLocatedToXpath('//*[@id="pw"]')

    #import platform
    #platform.system() return 'Windows'
    #diff key wid = CONTROL, mac = COMMAND

    input_id.click() 
    pyperclip.copy(naverInfo.ID) 
    input_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    input_pw.click() 
    pyperclip.copy(naverInfo.PW) 
    input_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    form = driverFindLocatedToXpath('//*[@id="frmNIDLogin"]')
    form.submit()

def naverSecondAuth():
    try:
        btn_sendAlt = driverFindClickAbleToXpath('//*[@id="resendBtn"]')
        btn_sendAlt.click()
    except:
        print("naverSecondAuth Except")


def naverPayAutoCheckout(payPassword):
    global isSuccess

    btn_Paid = driverFindClickAbleToXpath('//*[@id="root"]/div/div[3]/div/div/div[2]/button')
    btn_Paid.click()

    div_passwordMasking = driverFindLocatedToXpath('//*[@id="__next"]/div[2]/div/div/div/div[1]/div/div/div[2]/div[1]')
    
    locateArr = np.empty((0,2), float)

    _screen = np.array(pyautogui.screenshot())
    img = cv2.cvtColor(_screen, cv2.COLOR_RGB2GRAY)

    #cv2.imshow("result", _screen)
    #cv2.waitKey(0)

    for i in payPassword:
        target = cv2.imread(f'image/{i}.png', cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)

        minValue, maxValue, minLoc, maxLoc = cv2.minMaxLoc(result)

        width_center = maxLoc[0] + (target.shape[1] / 2)
        height_center = maxLoc[1] + (target.shape[0] / 2)

        locateArr = np.append(locateArr, np.array([[width_center, height_center]]), axis=0)
        
        #leftTop = maxLoc
        #print(minValue, maxValue, minLoc, maxLoc)
        #rightBottom = maxLoc[0]+ target.shape[1], maxLoc[1] + target.shape[0]
        #cv2.rectangle(_screen, leftTop, rightBottom, (255,255,0), 3)

    # cv2.imshow("result", _screen)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    for x in locateArr:
        # print(x)
        pyautogui.moveTo(x[0], x[1])
        pyautogui.click()
    
    isSuccess = True

def postMessage(message):
    global slack_client
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    # 로컬에서만 파이썬 셀 출력
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    print(strbuf)
    response = slack_client.chat_postMessage(
        channel='abstract-robot',
        text = strbuf
    )


driver = webdriver.Chrome()
driver.get("https://etk.srail.kr/main.do")


login(config.SRT_INFO)
searchTrainList(config.SRT_INFO)

postMessage('SRT 자동 예약 실행')

btn_reservations = None

while isSuccess == False:
    process_hour = datetime.now().hour
    if(macro_Start_hour != process_hour):
        macro_Start_hour = process_hour
        postMessage("SRT 자동 예약 실행중..\\")

    if(refreshCnt % 10 == 0):
        now = datetime.now()
        diff = now - macro_Start_Date
        print(f'refresh: {refreshCnt} - d: {diff.days} / h: {round(diff.seconds / 3600)} / m: {round(diff.seconds / 60)}')

    for i in range(1, config.SRT_INFO.LIST_ROW_COUNT+1):
        try:
            td = driverFindLocatedToXpath(f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[7]')
            span = td.find_element(By.TAG_NAME, 'span')
            spanTxt = span.get_attribute('innerHTML')
            if(spanTxt != '매진'):
                print(spanTxt)
                #postMessage(spanTxt)
            btn_reservations = td.find_elements(By.TAG_NAME, 'a')
        except NoSuchElementException:
            print("--------NoSuchElementException--------")
            td = None
            btn_reservations = None
            continue
        except StaleElementReferenceException:
            print("--------StaleElementReferenceException--------")
            td = None
            btn_reservations = None
            continue 
        except Exception as ex:
            print("except", ex)
            searchTrainList(config.SRT_INFO)

        if(btn_reservations != None and len(btn_reservations) > 1):
            btn_reservations[0].click()
            postMessage('티켓 발견 예약 진행')
            reservation(config.SRT_INFO.SECOND_PASSENGER_NAME)
            time.sleep(1)
            naverLogin(config.NAVER_INFO)
            time.sleep(1)
            naverSecondAuth()
            time.sleep(1)
            naverPayAutoCheckout(config.NAVER_INFO.PAY_PW)
            postMessage("예약 완료!")
            break

    if isSuccess == True:
        break

    try:
        researchTrainList()
    except:
        searchTrainList(config.SRT_INFO)

    time.sleep(0.7)

postMessage('SRT 자동 예약 종료')
input()