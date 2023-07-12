import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from testCases import Input_File


class Navigate_WiFi:
    menu_WiFi_xpath = '//*[@id="group_2"]'
    menu_wireless_xpath = '//*[@id="idx_44"]'
    menu_GuestWiFi_xpath = '//*[@id="idx_49"]/a'
    text_WirelessTitle_xpath = '//*[@id="contentbody"]/form/table/tbody/tr[1]/td/p'
    button_BandSteeringStatus_xpath = '//*[@id="band_steering_on"]'
    button_2GHzGuest1Edit_xpath = '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[' \
                                  '1]/td/table/tbody/tr/td/table/tbody/tr[2]/td[4]/div/a/span[2] '
    button_2GHzGuest2Edit_xpath = '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[' \
                                  '1]/td/table/tbody/tr/td/table/tbody/tr[3]/td[4]/div/a/span[2] '
    button_5GHzGuest1Edit_xpath = '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[' \
                                  '2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[4]/div/a/span[2] '
    button_5GHzGuest2Edit_xpath = '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[' \
                                  '2]/td/table/tbody/tr/td/table/tbody/tr[3]/td[4]/div/a/span[2] '
    textbox_2GHzSsid_xpath = '//*[@id="wl_ssid24G"]'
    textbox_5GHzSsid_xpath = '//*[@id="wl_ssid5G"]'
    textbox_SsidGuest_xpath = '//*[@id="gnset_table"]/td/table/tbody/tr[4]/td[2]/span/div/div/input'
    textbox_2GHzPwd_xpath = '//*[@id="sharedkey24G"]'
    textbox_5GHzPwd_xpath = ' //*[@id="sharedkey5G"]'
    textbox_PwdGuest_xpath = '//*[@id="sharedkey"]'
    button_SaveWirelessSetting_xpath = '//*[@id="save"]/span[2]'
    button_BroadcastStatus_xpath = '//*[@id="ssidhide24G"]'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def SelectMenuWiFi(self):
        self.driver.find_element(By.XPATH, self.menu_WiFi_xpath).click()

    def SelectSubMenuWireless(self, SSID_number):
        try:
            self.driver.find_element(By.XPATH, self.menu_wireless_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(3)
        except Exception as msg:
            print('Exception occurred')
        global GUI_SSID_Name
        if int(SSID_number) == 1:
            element = self.driver.find_element(By.XPATH, self.textbox_2GHzSsid_xpath)
            GUI_SSID_Name = element.get_attribute('value')
        elif int(SSID_number) == 4:
            element = self.driver.find_element(By.XPATH, self.textbox_5GHzSsid_xpath)
            GUI_SSID_Name = element.get_attribute('value')
        return GUI_SSID_Name

    def CheckSsidPwd(self, SSID_number):
        global GUI_Pwd_Name
        if int(SSID_number) == 1:
            element = self.driver.find_element(By.XPATH, self.textbox_2GHzPwd_xpath)
            GUI_Pwd_Name = element.get_attribute('value')
        elif int(SSID_number) == 4:
            element = self.driver.find_element(By.XPATH, self.textbox_5GHzPwd_xpath)
            GUI_Pwd_Name = element.get_attribute('value')
        return GUI_Pwd_Name

    def SelectSubMenuGuestWiFi(self, SSID_number):
        self.driver.find_element(By.XPATH, self.menu_GuestWiFi_xpath).click()
        time.sleep(2)
        self.driver.switch_to.frame('frm_main2')
        time.sleep(3)

        if int(SSID_number) == 2:
            self.driver.find_element(By.XPATH, self.button_2GHzGuest1Edit_xpath).click()
        elif int(SSID_number) == 3:
            self.driver.find_element(By.XPATH, self.button_2GHzGuest2Edit_xpath).click()
        elif int(SSID_number) == 5:
            self.driver.find_element(By.XPATH, self.button_5GHzGuest1Edit_xpath).click()
        elif int(SSID_number) == 6:
            self.driver.find_element(By.XPATH, self.button_5GHzGuest2Edit_xpath).click()
        element = self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath)
        GUI_SSID_Name = element.get_attribute('value')
        element1 = self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath)
        GUI_Pwd = element1.get_attribute('value')
        return GUI_SSID_Name, GUI_Pwd

    def GetBandSteeringStatus(self):
        global var
        self.driver.find_element(By.XPATH, self.menu_wireless_xpath).click()
        time.sleep(2)
        self.driver.switch_to.frame('frm_main2')
        time.sleep(3)
        element_value = self.driver.find_element(By.XPATH, self.text_WirelessTitle_xpath).text
        if element_value == '2.4GHz & 5GHz':
            var = 1
        elif element_value == '2.4GHz':
            var = 0
        return var

    def DisableBandSteering(self):
        self.driver.find_element(By.XPATH, self.button_BandSteeringStatus_xpath).click()
        self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()

    def SetSSIDFromGui(self, SSID_number):
        global GUI_SSIDName, GUI_Pwd
        self.driver.find_element(By.XPATH, self.menu_WiFi_xpath).click()
        time.sleep(2)

        if int(SSID_number) == 1:
            self.driver.find_element(By.XPATH, self.menu_wireless_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.textbox_2GHzSsid_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_2GHzSsid_xpath).send_keys(Input_File.SSID_AP1[1])
            self.driver.find_element(By.XPATH, self.textbox_2GHzPwd_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_2GHzPwd_xpath).send_keys(Input_File.SSID_Pwd_AP1[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_2GHzSsid_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_2GHzPwd_xpath).get_attribute('value')

        elif int(SSID_number) == 4:
            self.driver.find_element(By.XPATH, self.menu_wireless_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.textbox_5GHzSsid_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_5GHzSsid_xpath).send_keys(Input_File.SSID_AP4[1])
            self.driver.find_element(By.XPATH, self.textbox_5GHzPwd_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_5GHzPwd_xpath).send_keys(Input_File.SSID_Pwd_AP4[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_5GHzSsid_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_5GHzPwd_xpath).get_attribute('value')

        elif int(SSID_number) == 2:
            self.driver.find_element(By.XPATH, self.menu_GuestWiFi_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(3)
            self.driver.find_element(By.XPATH, self.button_2GHzGuest1Edit_xpath).click()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).send_keys(Input_File.SSID_AP2[1])
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).send_keys(Input_File.SSID_Pwd_AP2[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            self.driver.find_element(By.XPATH, self.button_2GHzGuest1Edit_xpath).click()
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).get_attribute('value')

        elif int(SSID_number) == 3:
            self.driver.find_element(By.XPATH, self.menu_GuestWiFi_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(3)
            self.driver.find_element(By.XPATH, self.button_2GHzGuest2Edit_xpath).click()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).send_keys(Input_File.SSID_AP3[1])
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).send_keys(Input_File.SSID_Pwd_AP3[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            self.driver.find_element(By.XPATH, self.button_2GHzGuest2Edit_xpath).click()
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).get_attribute('value')

        elif int(SSID_number) == 5:
            self.driver.find_element(By.XPATH, self.menu_GuestWiFi_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(3)
            self.driver.find_element(By.XPATH, self.button_5GHzGuest1Edit_xpath).click()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).send_keys(Input_File.SSID_AP5[1])
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).send_keys(Input_File.SSID_Pwd_AP5[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            self.driver.find_element(By.XPATH, self.button_5GHzGuest1Edit_xpath).click()
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).get_attribute('value')

        elif int(SSID_number) == 6:
            self.driver.find_element(By.XPATH, self.menu_GuestWiFi_xpath).click()
            time.sleep(2)
            self.driver.switch_to.frame('frm_main2')
            time.sleep(3)
            self.driver.find_element(By.XPATH, self.button_5GHzGuest2Edit_xpath).click()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).send_keys(Input_File.SSID_AP6[1])
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).send_keys(Input_File.SSID_Pwd_AP6[1])
            self.driver.find_element(By.XPATH, self.button_SaveWirelessSetting_xpath).click()
            time.sleep(30)
            self.driver.find_element(By.XPATH, self.button_5GHzGuest2Edit_xpath).click()
            GUI_SSIDName = self.driver.find_element(By.XPATH, self.textbox_SsidGuest_xpath).get_attribute('value')
            GUI_Pwd = self.driver.find_element(By.XPATH, self.textbox_PwdGuest_xpath).get_attribute('value')

        return GUI_SSIDName, GUI_Pwd
