import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from selenium.webdriver.remote.webelement import WebElement


class Advanced_View:
    menu_advancedView_xpath = '//*[@id="tblLeftMenu"]/tbody/tr[6]/td[2]'
    textbox_deviceTreeSearch_xpath = '//*[@id="txbFind"]'
    button_search_xpath = '//*[@id="btnFind_btn"]'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def ClickAdvancedView(self):
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.menu_advancedView_xpath).click()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)

    def SwitchFrame(self, frameId):
        time.sleep(2)
        self.driver.switch_to.frame(frameId)
        time.sleep(2)

    def SwitchToDefault(self):
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)

    def SearchTreeElement(self, Value):
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(Value)
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
