# -*- coding: utf-8 -*-
from selenium import webdriver
from collections import ChainMap
import json
from collections import OrderedDict
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import os
import re
import sys
from getpass import getpass
import User_Input
from collections import defaultdict
from pyvirtualdisplay import Display

fabirc_user = os.getenv('FABRICUSER')
fabirc_password = os.getenv('FABRICPASSWORD')

pgk = os.getenv('PGPKG')


github_account = fabirc_user
github_passwd = fabirc_password
print('MarkTest ' + github_account)

'''原始存放的資料'''
Crash = []
User = []
Version = []
IssueNumber = []
IssueTitle = []
IssueSubtitle = []
TestAll = []
URL = []
CrashTitle = []
UserTitle = []
VersionTitle = []
IssueNumberTitle = []
IssueTitleTitle = []
IssueSubtitleTitle = []
TestAllTitle = []
URLTitle = []
GetUserNumberTest = []

'''A代表再次重新放入新的字串'''
IssueNumberA = []
IssueTitleA = []
IssueSubtitleA = []
VersionA = []
CrashA = []
UserA = []
URLA = []
TestAllA = []
TestAllDictA = []
VersionA = []
AllUserSessionsA = []
AllUserSessionsNameA = []
SelectVersionA = []
SessionsA = []

'''檔案存到data字串中'''
data = []
dataDict = {}

'''取得全部的崩潰率'''
AllUserSessions = []
AllUserSessionsName = []

Top_build = User_Input.Top_build
SelectVersion = User_Input.Version
PlatformName = User_Input.PlatformName




RecentActivityVersion = []
RecentActivityVersionTitle = []
RecentActivityOccurrences = []
RecentActivityOccurrencesTitle = []


RecentActivityOccurrencesA = []
RecentActivityVersionA = []

RecentActivity = []
RecentActivityDict = {}




GetGoodAdoptionURLTest = []

class GithubLogin(unittest.TestCase):
    def setUp(self):
        self.display = Display(visible=0, size=(1920, 1080))
        self.display.start()
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.fabric.io"
        self.verificationErrors = []
        self.accept_next_alert = True

    def JSonFile(self, file):
        '''
         讀取檔案將參數放入到ADJson()內是你要丟入的檔案
         範例：
         ADJson = JSonFile('536_default.json')
        '''
        with open(file, 'r', encoding='utf-8')as f:  # 3.5
            ADJson = json.load(f, object_pairs_hook=OrderedDict)
        return ADJson


    def Platform(self, PlatformName):
        PlatformCss = self.driver.find_elements_by_css_selector('.js-app-view span')
        PlatformNumber = 0
        print("你選擇的平台是" + PlatformName)
        for i in PlatformCss:
            try:
                if i.text == PlatformName:
                    PlatformCss[PlatformNumber].click()
            except:
                pass
            PlatformNumber += 1
        time.sleep(5)

    def ClickCarshlytics(self):

        self.driver.find_element_by_css_selector(".crashlytics i").click()
        time.sleep(5)


    def EnterVserion(self,Version):
        print("你選擇的版本:")
        for i in range(len(Version)):
            print(Version[i])

        for i in range(len(Version)):
            VersionCheck = self.driver.find_elements_by_css_selector(".Select-arrow-zone span")
            VersionCheck[0].click()
            self.driver.find_element_by_class_name('Select-control').send_keys(Version[i] + '\n')
            time.sleep(3)



    def ClearSelectIcon(self):

        # 清掉預設值
        self.driver.find_element_by_class_name('Select-value-icon').click()
        time.sleep(5)

    def SelectAll(self):
        # ClickAll = self.driver.find_elements_by_css_selector("#state-group-all")
        self.driver.find_element_by_id("state-group-all").click()
        time.sleep(5)
        print("點擊All")

    def ReadAllUserSessions(self):

        All = self.driver.find_elements_by_css_selector('.crash-free-percent .stat .value')
        Name = self.driver.find_elements_by_css_selector('.crash-free-percent .stat .name')
        for i in All:
            AllUserSessions.append(i.text)

        for i in Name:
            AllUserSessionsName.append(i.text)

    def MoveWeb(self):

        # 向下滑動判斷150筆停止
        print("正在滑動頁面請稍等...")
        # AllNumber = self.driver.find_elements_by_css_selector(".events-stat span span")
        for i in range(5):
            # if int(len(AllNumber)) == 180:
            #     pass
            # else:
            js = "var q=document.documentElement.scrollTop=10000"
            self.driver.execute_script(js)
            time.sleep(5)

    def ReadUrl(self):

        #讀取URL 數量
        print("開始-->讀取URL")
        URLNumber  = self.driver.find_elements_by_css_selector(".cell-title a")
        for i in URLNumber:
            URL.append(i.get_attribute("href"))
            URLTitle.append("URL")
        print("結束-->讀取URL")

    def ReadCrashNumber(self):

        # 讀取Crash 數量
        print("*"*10)
        print("開始-->讀取Crash數量")
        CrashNumber = self.driver.find_elements_by_css_selector(".events-stat span span")
        for i in CrashNumber:
            if i.text == 'CRASHES':
                pass
            elif i.text == 'CRASH':
                pass
            elif i.text == '':
                pass
            else:
                Crash.append(i.text)
                CrashTitle.append(("Crash"))
        print("結束-->讀取Crash數量")
        print("*"*10)

    def ReadUserNumber(self):
        # 讀取User 數量
        print("開始-->讀取User數量")
        UserNumber = self.driver.find_elements_by_css_selector(".devices-stat span span")

        for i in UserNumber:
            if i.text =='USERS':
                pass
            elif i.text == '':
                pass
            elif i.text =='USER':
                pass
            else:
                User.append(i.text)
                UserTitle.append("User")
        print("結束-->讀取User數量")
        print("*"*10)

    def ReadVersionNumber(self):
        # 讀取發生的版本號
        print("開始-->讀取Version")
        VersionNumber  = self.driver.find_elements_by_css_selector(".more-info")
        for i in VersionNumber:
            Version.append(i.text)
            VersionTitle.append("Version")
        print("結束-->讀取Version")
        print("*"*10)
    def ReadIssueNumber(self):
        # Issue 數字
        print("開始-->讀取Issue編號")
        IssueNumberTest = self.driver.find_elements_by_css_selector(".issue-number")
        for i in IssueNumberTest:
            IssueNumber.append(i.text)
            IssueNumberTitle.append("IssueNumber")
        print("結束-->讀取Issue編號")
        print("*"*10)
    def ReadIssueTitle(self):
        # Issue 開頭
        print("開始-->讀取Issue開頭")
        IssueTitleTest = self.driver.find_elements_by_css_selector(".issue-title")
        for i in IssueTitleTest:
            IssueTitle.append(i.text)
            IssueTitleTitle.append("IssueTitle")
        print("結束-->讀取Issue開頭")
        print("*"*10)
    def ReadIssueSubtitle(self):
        # Issue 大綱
        print("開始-->讀取Issue大綱")
        IssueSubtitleTest = self.driver.find_elements_by_css_selector(".issue-subtitle")
        for i in IssueSubtitleTest:
            IssueSubtitle.append(i.text)
            IssueSubtitleTitle.append("IssueSubtitle")
        print("結束-->讀取Issue大綱")
        print("*"*10)
    def ReadAllNumber(self):
        IssueAllNumber = len(IssueSubtitle)
        x = 1
        for i in range(IssueAllNumber):
            TestAll.append(x)
            TestAllTitle.append("Rank")
            x += 1

    def Get_RecentActivity(self):
        self.DefaultValue()
        RecentActivity = self.driver.find_elements_by_css_selector(".padding-left-15px tbody td")
        # print(len(RecentActivityOccurrences))
        x = 1
        for i in RecentActivity:
            if x % 2 == 0:
                RecentActivityOccurrences.append(i.text)
                RecentActivityOccurrencesTitle.append('Occurrences')
            else:
                RecentActivityVersion.append(i.text)
                RecentActivityVersionTitle.append('Version')
            x += 1
    def ListToJsonFile(self, FileName):

        print("開始-->將資料轉成Json")


        for i in range(len(IssueNumber)):

            '''先將原本的字串另存到新的空字串中'''
            IssueNumberA.append(IssueNumber[i])
            IssueTitleA.append(IssueTitle[i])
            IssueSubtitleA.append(IssueSubtitle[i])
            VersionA.append(Version[i])
            CrashA.append(Crash[i])
            UserA.append(User[i])
            URLA.append(URL[i])
            TestAllA.append(TestAll[i])

            '''將兩個字串合併成字典'''
            TestAllDict = OrderedDict(zip(TestAllTitle, TestAllA))
            IssueNumberDict = OrderedDict(zip(IssueNumberTitle, IssueNumberA))
            IssueTitleDict = OrderedDict(zip(IssueTitleTitle, IssueTitleA))
            IssueSubtitleDict = OrderedDict(zip(IssueSubtitleTitle, IssueSubtitleA))
            VersionDict = OrderedDict(zip(VersionTitle, VersionA))
            CrashDict = OrderedDict(zip(CrashTitle, CrashA))
            UserDict = OrderedDict(zip(UserTitle, UserA))
            URLDict = OrderedDict(zip(URLTitle, URLA))

            '''每次字典更新新增一筆'''
            TestAllDict.update(IssueNumberDict)
            TestAllDict.update(IssueTitleDict)
            TestAllDict.update(IssueSubtitleDict)
            TestAllDict.update(VersionDict)
            TestAllDict.update(CrashDict)
            TestAllDict.update(UserDict)
            TestAllDict.update(URLDict)
            data.append(TestAllDict)
            dataDict['data'] = data

        # '''將字典存成Json'''
        with open(FileName, 'w') as f:
            json.dump(dataDict, f)
        f.close()
        print("結束-->將資料轉成Json")
        print("*"*10)
        print("請查看" + FileName)

    def ListToJsonFile_Crash(self, FileName):
        print("開始-->將資料轉成Json")
        User_Input.Version.append('All Version')
        itmes = 0
        Test = len(AllUserSessions)//2
        User = len(GetUserNumberTest)

        for i in range(Test):
            # 主要是新增崩潰量 因為一次抓取兩個參數值
            # 一開始會先執行else部分之後都會去執行i >=1
            if i >= 1:
                itmes += 1
                AllUserSessionsA.append(AllUserSessions[i + itmes])
                AllUserSessionsNameA.append(AllUserSessionsName[i + itmes])
                AllUserSessionsA.append(AllUserSessions[i + itmes + 1])
                AllUserSessionsNameA.append(AllUserSessionsName[i + itmes + 1])
            else:
                AllUserSessionsA.append(AllUserSessions[i])
                AllUserSessionsNameA.append(AllUserSessionsName[i])
                AllUserSessionsA.append(AllUserSessions[i + 1])
                AllUserSessionsNameA.append(AllUserSessionsName[i + 1])

            # 主要是判斷使用者的人數 如果超過某區塊會將使用者人數設定為Null.
            if i > (User-1):
                # AllUserSessionsA.append('Null')
                # AllUserSessionsNameA.append('User')
                pass
            else:
                AllUserSessionsA.append(GetUserNumberTest[i])
                AllUserSessionsNameA.append('User')

            Sessions = OrderedDict(zip(AllUserSessionsNameA, AllUserSessionsA))
            SessionsA.append(Sessions)

        Get_crash_free_session = OrderedDict(zip(User_Input.Version, SessionsA))

        '''將字典存成Json'''
        with open(FileName, 'w') as f:
            json.dump(Get_crash_free_session, f)
        f.close()
        print("結束-->將資料轉成Json")
        print("*"*10)
        print("請查看" + FileName)


    def test_Read_Fabirc(self):
        print('Top build version query raw data')

        driver = self.driver
        driver.get(self.base_url + "/login")

        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(github_account)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(github_passwd)
        driver.find_element_by_class_name("sign-in").click()
        time.sleep(5)

        # iOS or Android
        self.Platform(PlatformName)  # Sean
        self.ClickCarshlytics()
        self.EnterVserion(Top_build)  # Sean
        self.ClearSelectIcon()
        self.SelectAll()
        self.ReadAllUserSessions()
        self.MoveWeb()
        self.ReadUrl()
        self.ReadCrashNumber()
        self.ReadUserNumber()
        self.ReadVersionNumber()
        self.ReadIssueNumber()
        self.ReadIssueTitle()
        self.ReadIssueSubtitle()
        self.ReadAllNumber()
        self.ListToJsonFile('Top_build_Fabric.json')

        print("Get Recent Activity")
        time.sleep(2)
        ADJson = self.JSonFile('Top_build_Fabric.json')

        # driver.get(ADJson['data'][0]['URL'])
        # self.Get_RecentActivity()

        for i in range(len(ADJson['data'])):
            driver.get(ADJson['data'][i]['URL'])
            self.Get_RecentActivity()

            for j in range(len(RecentActivityOccurrences)):
                RecentActivityOccurrencesA.append(RecentActivityOccurrences[j])
                RecentActivityVersionA.append(RecentActivityVersion[j])

                '''將兩個字串合併成字典'''
                RecentActivityOccurrencesDict = OrderedDict(
                    zip(RecentActivityOccurrencesTitle, RecentActivityOccurrencesA))
                RecentActivityVersionDict = OrderedDict(zip(RecentActivityVersionTitle, RecentActivityVersionA))

                '''每次字典更新新增一筆'''
                RecentActivityVersionDict.update(RecentActivityOccurrencesDict)
                RecentActivity.append(RecentActivityVersionDict)
                RecentActivityDict['RecentActivity'] = RecentActivity
                ADJson['data'][i].update(RecentActivityDict)


                # RecentActivityDict = {}

        with open('Top_build_Fabric.json', 'w') as f:
            json.dump(ADJson, f)
        f.close()
        print("結束-->將資料轉成Json")
        print("*" * 10)
        print("請查看" + 'Top_build_Fabric.json')


    def test_Carsh_Top(self):
        print('Get crash-free session only')

        driver = self.driver
        driver.get(self.base_url + "/login")

        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(github_account)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(github_passwd)
        driver.find_element_by_class_name("sign-in").click()
        driver.save_screenshot('Mark.png')
        time.sleep(5)
        self.Platform(PlatformName)  # Sean
        self.ClickCarshlytics()

        for i in range(len(SelectVersion)):
            SelectVersionA.append(SelectVersion[i])

            self.EnterVserion(SelectVersionA)  # Sean
            self.ClearSelectIcon()
            self.ReadAllUserSessions()
            # self.GetGoodAdoptionURLfunction()

            SelectVersionA.pop()

            # 讀取 All Verison
        print("你選擇的版本:\nAll Version")
        self.ClearSelectIcon()
        self.ReadAllUserSessions()
        GetUserNumberTest.append("Null")
        self.GetGoodAdoptionUserNumber()
        # self.GetGoodAdoptionURLfunction()
        #
        # for i in range(len(GetGoodAdoptionURLTest)):
        #
        #     if GetGoodAdoptionURLTest[i] is 'Null':
        #         GetUserNumberTest.append('Null')
        #     else:
        #         self.driver.get(GetGoodAdoptionURLTest[i])
        #         time.sleep(15)
        #         self.driver.save_screenshot(str([i]) + 'Mark.png')
        #         self.GetGoodAdoptionUserNumber()

        # 查詢前幾版的崩潰狀況
        self.ListToJsonFile_Crash('Fabric.json')


    def GetGoodAdoptionUserNumber(self):
        UserURL = "https://www.fabric.io/photogrid/android/apps/" + pgk + "/dashboard/latest_release/launch_status?build="


        print("你選擇的版本:")
        for i in range(len(SelectVersion)):
            print(SelectVersion[i])

        for i in range(len(SelectVersion)):
            self.driver.get(UserURL + SelectVersion[i])
            time.sleep(5)



            GetUserNumber = self.driver.find_elements_by_css_selector(".coverage-section .flex-1 .flex-1 .large")
            print('GetUserNumber : ' + GetUserNumber)
            x = 0
            for y in GetUserNumber:
                x += 1
                if x == 1:
                    GetUserNumberTest.append(str(y.text))
                    print("get user")
                    print(str(y.text))

            time.sleep(3)


    def GetGoodAdoptionURLfunction(self):
        GetGoodAdoptionURL = self.driver.find_elements_by_css_selector('.flex-1 .answers-link')
        TestList = []
        # 判斷如果沒有連結會自動帶入Null
        if GetGoodAdoptionURL == TestList:
            GetGoodAdoptionURLTest.append('Null')
        for i in GetGoodAdoptionURL:
            GetGoodAdoptionURLTest.append(i.get_attribute("href"))
            print("get href")
            print(i.get_attribute("href"))




    def DefaultValue(self):
        global RecentActivityOccurrencesA, RecentActivityVersionA, RecentActivityOccurrences, RecentActivityVersion, \
            RecentActivityDict, RecentActivity
        RecentActivityOccurrencesA = []
        RecentActivityVersionA = []
        RecentActivityOccurrences = []
        RecentActivityVersion = []
        RecentActivityDict = {}
        RecentActivity = []


    def tearDown(self):
        self.driver.quit()
        self.display.stop()


if __name__ == "__main__":
    unittest.main()
