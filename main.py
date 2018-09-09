# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sys
import make_csv as m
import crawler_config as cc
import stores as s
import cities as c

delay = 0
driver = None
count_start = 0
count_end = 0
store_infos = []

#중복되는 주소를 위한 리스트
store_addresses = []

def init():
    global driver
    driver = webdriver.Chrome("./driver/chromedriver")

def init_headless():
    global driver
    driver = cc.initCrawler()

def getCount(query):
    global driver
    global delay
    global store_infos
    driver.get("http://map.daum.net")
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        if len(count.text) > 3:
            return True
        else:
            if count.text == '':
                totCount = 0
            else:
                totCount = int(count.text, base=10)
            if totCount > 525:
                return True
            else:
                return False



def crawlList(query, city = ""):

    print("now program crawls data....")
    global store_addresses
    global count_start
    global count_end
    global store_infos
    _html = driver.page_source
    soup = BeautifulSoup(_html, "lxml")
    for e in soup.find_all("li", class_="PlaceItem"):
        tempClass = s.storeInfoClass()
        tempName = e.h6.a["title"]
        realName = tempName.split(" ")
        tfAddress = e.find("span", class_="subAddress")
        hasNotAddress= 1
        for i in range(0, len(store_infos)) :
            if tfAddress != None:
                if tfAddress.text == store_infos[i].getAddress().decode('euc-kr'):
                    hasNotAddress = 0
        if hasNotAddress == 1 and realName[0] == query:
            tempClass.setName(realName[0].encode('euc-kr'))
            tempAddress = e.find("span", class_="subAddress")
            branch = ""
            if len(realName) != 2:
                if tempAddress != None and (tempAddress.text not in store_addresses):
                    for i in range(1, len(realName)):
                        branch = branch + ' ' + realName[i]
                else :
                    continue
            else :
                branch = realName[1]
            tempClass.setBranch(branch.encode('euc-kr'))
            tempPhoneNum = e.find("span", class_="phone")
            tempClass.setPhoneNum(tempPhoneNum.text.encode('euc-kr'))

            if tempAddress != None:
                store_addresses.append(tempAddress.text)
                if city != "":
                    newAddress = city + tempAddress.text
                else: 
                    newAddress = tempAddress.text
                tempClass.setAddress(newAddress.encode('euc-kr'))
                store_infos.append(tempClass)
            else :
                tempClass.setAddress("Unknown".encode('euc-kr'))

            count_end += 1
        else:
            continue

    count_start = count_end

def getMapUnder525(query):
    global driver
    global delay
    global count_start
    global count_end
    global store_infos
    driver.get("http://map.daum.net")
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        if count.text != '':
            total_data_count = int(count.text)
        else :
            total_data_count = 0
        # crawlList(query)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.page.no1")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        finally:
            return total_data_count

def getMapOver525(query, locationQuery, city):
    global driver
    global delay
    global count_start
    global count_end
    global store_infos
    driver.get("http://map.daum.net")
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
    except TimeoutException:
        print("Loading took too much time!")
    finally:
        elem.clear()
        elem.send_keys(locationQuery)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        _html = driver.page_source
        soup = BeautifulSoup(_html, "lxml")
        count = soup.find("em", id="info.search.place.cnt")
        if count.text != '':
            total_data_count = int(count.text)
        else :
            total_data_count = 0

        #지역명 + 상호명 일 때는 2페이지부터 보여줌으로 한번 긁고 시작해야한다!
        crawlList(query, city)
        try:
            clickElem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
            clickElem.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            return total_data_count

def startCrawlingUnder525(query, totalDataCount):
    # ******1페이지에 15개의 정보!******
    global driver
    global count_start
    global count_end
    global delay
    global store_infos
    pagingString = "info.search.page.no"
    tempIntNum = int(totalDataCount/15)
    if totalDataCount % 15 != 0:
        totalPage = tempIntNum + 1
    else :
        totalPage = tempIntNum


    # 1페이지와 2페이지는 시작하면서 읽어내기 때문
    if totalPage >1 :
        # try:
        #     clickElem = WebDriverWait(driver, delay) \
        #         .until(EC.presence_of_element_located((By.ID, "info.search.place.more")))
        #     clickElem.click()
        #     time.sleep(1)
        # except TimeoutException:
        #     print("Loading took too much time!")

        crawlList(query)
        totalPageCount = totalPage - 1
        pageNo = 2

        while totalPageCount > 0 :
            if ((pageNo-1)%5) == 0: #arrow
                try:
                    clickElem = WebDriverWait(driver, delay) \
                        .until(EC.presence_of_element_located((By.ID, "info.search.page.next")))
                    clickElem.click()
                    time.sleep(1)
                    crawlList(query)
                except TimeoutException:
                    print("Loading took too much time. total page > 2!!!!")
                pageNo = 2
                totalPageCount -= 1
            else :  #now a arrow
                clickId = pagingString + str(pageNo)
                try:
                    clickElem = WebDriverWait(driver, delay) \
                        .until(EC.presence_of_element_located((By.ID, clickId)))
                    clickElem.click()
                    time.sleep(1)
                    crawlList(query)
                except TimeoutException:
                    print("Loading took too much time. total page > 2!!!!")
                pageNo += 1
                totalPageCount -= 1
    else :
        crawlList(query)

def startCrawlingOver525(query, totalDataCount):
    # ******1페이지에 15개의 정보!******
    global driver
    global count_start
    global count_end
    global delay
    global store_infos
    pagingString = "info.search.page.no"
    tempIntNum = int(totalDataCount/15)
    if totalDataCount % 15 != 0:
        totalPage = tempIntNum + 1
    else :
        totalPage = tempIntNum

    #2번째
    crawlList(query)


    totalPageCount = totalPage - 2
    pageNo = 3

    while totalPageCount > 0 :
        if ((pageNo-1)%5) == 0: #arrow
            try:
                clickElem = WebDriverWait(driver, delay) \
                   .until(EC.presence_of_element_located((By.ID, "info.search.page.next")))
                clickElem.click()
                time.sleep(1)
                crawlList(query)
            except TimeoutException:
                print("Loading took too much time. total page > 2!!!!")
            pageNo = 2
            totalPageCount -= 1
        else :  #now a arrow
            clickId = pagingString + str(pageNo)
            try:
                clickElem = WebDriverWait(driver, delay) \
                    .until(EC.presence_of_element_located((By.ID, clickId)))
                clickElem.click()
                time.sleep(1)
                crawlList(query)
            except TimeoutException:
                print("Loading took too much time. total page > 2!!!!")
            pageNo += 1
            totalPageCount -= 1

def printAllStores():
    for e in store_infos:
        print(str(e.getName()) + " <---> " + str(e.getBranch()) + " <---> " + str(e.getPhoneNum()) + " <---> " + str(e.getAddress()))



def main():

    init_headless()
    continueTf = True
    global store_infos
    while continueTf:
        store_infos = []
        query = input("상호명을 입력하세요: ")
        if getCount(query) == True:  # 525개 이상의 데이터
            for i in range(0, len(c.cities)):
                locationQuery = c.cities[i]+query
                totalDataCount = getMapOver525(query, locationQuery, c.cities[i])
                startCrawlingOver525(query, totalDataCount)
        else:  # 525개 미만의 데이터
            totalDataCount = getMapUnder525(query)
            if totalDataCount > 15:
                startCrawlingUnder525(query, totalDataCount)

        # printAllStores()
        # m.store_to_csv(store_infos)
        m.store_to_csv_pandas(store_infos)
        print("crawling data finish!")
        tf = input("검색을 계속 진행하시겠습니까? (y/n): ")
        if tf=='y':
            continueTf = True
        else:
            continueTf = False

    print("검색을 종료합니다.")
    print("Ctrl + C를 눌러 프로그램을 종료하세요!")


if __name__ == "__main__":
    main()


