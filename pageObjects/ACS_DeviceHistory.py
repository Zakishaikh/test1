import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class deviceHistory:
    menu_DeviceHistory_xpath = '//*[@id="tblLeftMenu"]/tbody/tr[14]/td[2]'
    dropdown_ActivityType_xpath = '//*[@id="ddlEvents"]'
    textbox_EventTime_xpath = '//*[@id="tblItems"]/tbody/tr[2]/td[2]/div'
    textbox_TotalEventCount = '//*[@id="pager2_lblCount"]'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def ClickDeviceHistory(self):
        element = self.driver.find_element(By.XPATH, self.menu_DeviceHistory_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH, self.menu_DeviceHistory_xpath).click()

    def SelectEvent(self,event):
        select = Select(self.driver.find_element(By.XPATH, self.dropdown_ActivityType_xpath))
        select.select_by_visible_text(event)

    def GetEventCount(self):
        element = self.driver.find_element(By.XPATH, self.textbox_TotalEventCount)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        eventCount = self.driver.find_element(By.XPATH, self.textbox_TotalEventCount).text
        return eventCount

    def GetEventGeneratedTime(self):
        TimeStamp = self.driver.find_element(By.XPATH, self.textbox_EventTime_xpath).text
        return TimeStamp

    