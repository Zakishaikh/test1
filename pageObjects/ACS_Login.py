import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class Login_ACS:
    textbox_username_xpath = '//*[@id="txtName"]'
    textbox_password_xpath = '//*[@id="txtPassword"]'
    button_login_xpath = '//*[@id="btnLogin_btn"]'
    menu_search_xpath = '//*[@id="tblLeftMenu"]/tbody/tr[2]/td[2]'
    dropdown_searchBy_xpath = '//*[@id="ddlSearchOption"]'
    search_box_xpath = '//*[@id="tbDeviceID"]'
    button_search_xpath = '//*[@id="btnSearch_btn"]'
    menu_deviceInfo_xpath = '//*[@id="tblLeftMenu"]/tbody/tr[4]/td[2]'
    button_factoryReset_xpath = '//*[@id="btnReset_btn"]'
    button_Reboot_xpath = '//*[@id="btnReboot_btn"]'
    button_AlertOk1_xpath = '//*[@id="btnOk_btn"]'
    button_AlertOk2_xpath = '//*[@id="btnAlertOk_btn"]'
    button_GPV_xpath = '//*[@id="UcDeviceSettingsControls1_btnGetCurrent_btn"]'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def SetUserName(self, username):
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.textbox_username_xpath)))
            print('Located Username')
        finally:
            self.driver.find_element(By.XPATH, self.textbox_username_xpath).clear()
            self.driver.find_element(By.XPATH, self.textbox_username_xpath).send_keys(username)
            print('Entered Username')

    def SetPassword(self, password):
        self.driver.find_element(By.XPATH, self.textbox_password_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_password_xpath).send_keys(password)
        # print('Entered Password')

    def ClickLogin(self):
        self.driver.find_element(By.XPATH, self.button_login_xpath).click()
        print('Clicked on Login Button')

    def SearchDevice(self):
        self.driver.find_element(By.XPATH, self.menu_search_xpath).click()
        print('Selected Search menu')
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        select = Select(self.driver.find_element(By.XPATH, self.dropdown_searchBy_xpath))
        select.select_by_visible_text('Serial Number')
        self.driver.find_element(By.XPATH, self.search_box_xpath).clear()
        self.driver.find_element(By.XPATH, self.search_box_xpath).send_keys(
            ReadConfig_ACS_Environment.getDeviceSerial())
        print('Entered Device Serial number')
        time.sleep(3)
        self.driver.find_element(By.XPATH, self.button_search_xpath).click()

    def DeviceInfo(self):
        self.driver.find_element(By.XPATH, self.menu_deviceInfo_xpath).click()

    def FactoryReset(self):
        self.driver.find_element(By.XPATH, self.button_factoryReset_xpath).click()

    def AcceptAlert1(self):
        self.driver.find_element(By.XPATH, self.button_AlertOk1_xpath).click()

    def AcceptAlert2(self):
        self.driver.find_element(By.XPATH, self.button_AlertOk2_xpath).click()

    def Reboot(self):
        self.driver.find_element(By.XPATH, self.button_Reboot_xpath).click()

    def GetCurrentParameter(self):
        self.driver.find_element(By.XPATH, self.button_GPV_xpath).click()


