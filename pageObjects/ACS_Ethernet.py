import time
from selenium import common
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from selenium.webdriver.remote.webelement import WebElement


class EthernetStats:
    textbox_BytesReceived_xpath = '//*[@id="tblParamsTable"]/tbody/tr[4]/td[2]/input'
    textbox_BytesSent_xpath = '//*[@id="tblParamsTable"]/tbody/tr[5]/td[2]/input'
    textbox_PacketsReceived_xpath = '//*[@id="tblParamsTable"]/tbody/tr[12]/td[2]/input'
    textbox_PacketsSent_xpath = '//*[@id="tblParamsTable"]/tbody/tr[13]/td[2]/input'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def GetBytesReceived_Stats(self):
        element = self.driver.find_element(By.XPATH, self.textbox_BytesReceived_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        Stats = self.driver.find_element(By.XPATH, self.textbox_BytesReceived_xpath).get_attribute('value')
        return Stats

    def GetBytesSent_Stats(self):
        element = self.driver.find_element(By.XPATH, self.textbox_BytesSent_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        Stats = self.driver.find_element(By.XPATH, self.textbox_BytesSent_xpath).get_attribute('value')
        return Stats

    def GetPacketsReceived_Stats(self):
        element = self.driver.find_element(By.XPATH, self.textbox_PacketsReceived_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        Stats = self.driver.find_element(By.XPATH, self.textbox_PacketsReceived_xpath).get_attribute('value')
        return Stats

    def GetPacketsSent_Stats(self):
        element = self.driver.find_element(By.XPATH, self.textbox_PacketsSent_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        Stats = self.driver.find_element(By.XPATH, self.textbox_PacketsSent_xpath).get_attribute('value')
        return Stats

