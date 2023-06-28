import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class ChangeTr069Parameters:
    AcsURL = 'http://iotacs.jioconnect.com:8080/ftacs-digest/ACS'
    AcsUser = 'RelianceJio'
    AcsPwd = 'Jdev_1214'
    textbox_AcsURL_xpath = '//*[@id="tr69table"]/tbody/tr[2]/td[2]/span/div/div/input'
    textbox_AcsUsername_xpath = '//*[@id="tr69table"]/tbody/tr[3]/td[2]/span/div/div/input'
    textbox_AcsPassword_xpath = '//*[@id="tr69table"]/tbody/tr[4]/td[2]/span/div/div/input'
    button_SaveSettings_xpath = '//*[@id="save"]/span[2]'
    textbox_PeriodicInform_xpath = '//*[@id="tr69table"]/tbody/tr[7]/td[2]/span/div/div/input'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def ChangeAcsUrl(self):
        self.driver.find_element(By.XPATH, self.textbox_AcsURL_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_AcsURL_xpath).send_keys(ChangeTr069Parameters.AcsURL)

    def ChangeAcsUsername(self):
        self.driver.find_element(By.XPATH, self.textbox_AcsUsername_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_AcsUsername_xpath).send_keys(ChangeTr069Parameters.AcsUser)

    def ChangeAcsPassword(self):
        self.driver.find_element(By.XPATH, self.textbox_AcsPassword_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_AcsPassword_xpath).send_keys(ChangeTr069Parameters.AcsPwd)

    def ChangePeriodicTime(self):
        self.driver.find_element(By.XPATH, self.textbox_PeriodicInform_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_PeriodicInform_xpath).send_keys('30')

    def SaveAcsSettings(self):
        self.driver.find_element(By.XPATH, self.button_SaveSettings_xpath).click()

    def CheckAcsParameter(self):
        acs_url = self.driver.find_element(By.XPATH, self.textbox_AcsURL_xpath).get_attribute('value')
        acs_user = self.driver.find_element(By.XPATH, self.textbox_AcsUsername_xpath).get_attribute('value')
        acs_pwd = self.driver.find_element(By.XPATH, self.textbox_AcsPassword_xpath).get_attribute('value')
        return acs_url, acs_user, acs_pwd


