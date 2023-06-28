import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class Navigate_Overview:
    menu_Overview_xpath = '//*[@id="group_0"]/a'
    menu_NetworkStatus_xpath = '//*[@id="idx_4"]/a'
    text_BroadcastStatusAp1_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[2]/td[5]'
    text_BroadcastStatusAp2_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[3]/td[5]'
    text_BroadcastStatusAp3_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[4]/td[5]'
    text_BroadcastStatusAp4_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[5]/td[5]'
    text_BroadcastStatusAp5_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[6]/td[5]'
    text_BroadcastStatusAp6_xpath = '//*[@id="tb_wlan_status"]/tbody/tr[7]/td[5]'
    menu_RouterInformation_xpath = '//*[@id="idx_9"]/a'
    text_DeviceUptime = '//*[@id="uptime"]'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def SelectMenuOverview(self):
        self.driver.find_element(By.XPATH, self.menu_Overview_xpath).click()

    def SelectSubMenu_NetworkStatus(self):
        self.driver.find_element(By.XPATH, self.menu_NetworkStatus_xpath).click()
        time.sleep(2)
        self.driver.switch_to.frame('frm_main2')
        time.sleep(3)

    def GetBroadcastStatus(self, SSID_number):
        # element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp1_xpath)
        # actions = ActionChains(self.driver)
        # actions.move_to_element(element).perform()
        if int(SSID_number) == 1:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp1_xpath)
            BroadcastStatus_GUI = element.text
        elif int(SSID_number) == 2:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp2_xpath)
            BroadcastStatus_GUI = element.text
        elif int(SSID_number) == 3:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp3_xpath)
            BroadcastStatus_GUI = element.text
        elif int(SSID_number) == 4:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp4_xpath)
            BroadcastStatus_GUI = element.text
        elif int(SSID_number) == 5:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp5_xpath)
            BroadcastStatus_GUI = element.text
        elif int(SSID_number) == 6:
            element = self.driver.find_element(By.XPATH, self.text_BroadcastStatusAp6_xpath)
            BroadcastStatus_GUI = element.text

        return BroadcastStatus_GUI

    def SelectSubMenu_RouterInformation(self):
        self.driver.find_element(By.XPATH, self.menu_RouterInformation_xpath).click()

    def CheckDeviceUptime(self):
        systemUptime = self.driver.find_element(By.XPATH, self.text_DeviceUptime).text
        return systemUptime
