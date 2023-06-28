import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class Login_GUI:
    textbox_username_xpath = '//*[@id="login_field"]/table/tbody/tr[3]/td[3]/span/div/div/input'
    textbox_password_xpath = '//*[@id="login_field"]/table/tbody/tr[4]/td[3]/span/div/div/input'
    button_login_xpath = '//*[@id="btn_"]/a/span[2]'
    button_logout_xpath = '//*[@id="btn_logout"]'
    text_loginPage = '//*[@id="960001"]'
    textbox_NewPassword_xpath = '//*[@id="login_field"]/table/tbody/tr[3]/td[3]/span/div/div/input'
    textbox_ConfirmPassword_xpath = '//*[@id="login_field"]/table/tbody/tr[4]/td[3]/span/div/div/input'
    button_savePwdSetting_xpath = '//*[@id="save"]/span[2]'

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
        print('Clicked of Login Button')

    def login_exception(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def SwitchFrame(self, frameId):
        time.sleep(2)
        self.driver.switch_to.frame(frameId)
        time.sleep(2)

    def SwitchToDefault(self):
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)

    def ClickLogout(self):
        self.driver.find_element(By.XPATH, self.button_logout_xpath).click()

    def ChangeGUIPwd(self,pwd):
        self.driver.find_element(By.XPATH, self.textbox_NewPassword_xpath).send_keys(pwd)
        self.driver.find_element(By.XPATH, self.textbox_ConfirmPassword_xpath).send_keys(pwd)
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_savePwdSetting_xpath).click()



