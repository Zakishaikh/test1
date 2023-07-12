import time
from selenium import common
from utilities.ReadAcsTree import ReadConfig_ACS_Tree
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from testCases import Input_File


class acsWifi:
    textbox_deviceTreeSearch_xpath = '//*[@id="txbFind"]'
    button_search_xpath = '//*[@id="btnFind_btn"]'
    button_edit_xpath = '//*[@id="UcDeviceSettingsControls1_btnChange_btn"]'
    textbox_SSID_xpath = '//*[@id="tblParamsTable"]/tbody/tr[9]/td[2]/input'
    textbox_Security_xpath = '//*[@id="tblParamsTable"]/tbody/tr[2]/td[2]/input'
    button_sendUpdate_xpath = '//*[@id="UcDeviceSettingsControls1_btnSendUpdate_btn"]'
    button_Alert_xpath = '//*[@id="btnOk_btn"]'
    button_alert_xpath = '//*[@id="btnAlertOk_btn"]'
    textbox_ApStatus_xpath = '//*[@id="tblParamsTable"]/tbody/tr[5]/td[2]/input'
    textbox_ApEnable_xpath = '//*[@id="tblParamsTable"]/tbody/tr[5]/td[2]/input'
    textbox_SSIDBroadcast_xpath = '//*[@id="tblParamsTable"]/tbody/tr[10]/td[2]/input'

    # //*[@id="txtVal526"]

    def __init__(self, driver):
        self.SSID_Pwd = None
        self.element_security = None
        self.element_ssid = None
        self.element_ap = None
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def Get_ElementId(self, SSID_number):
        if SSID_number == 1:
            self.element_ap = ReadConfig_ACS_Tree.getAp1()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID1()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd1()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP1[0]
        elif SSID_number == 2:
            self.element_ap = ReadConfig_ACS_Tree.getAp2()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID2()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd2()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP2[0]
        elif SSID_number == 3:
            self.element_ap = ReadConfig_ACS_Tree.getAp3()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID2()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd3()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP3[0]
        elif SSID_number == 4:
            self.element_ap = ReadConfig_ACS_Tree.getAp4()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID2()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd4()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP4[0]
        elif SSID_number == 5:
            self.element_ap = ReadConfig_ACS_Tree.getAp5()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID2()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd5()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP5[0]
        elif SSID_number == 6:
            self.element_ap = ReadConfig_ACS_Tree.getAp6()
            self.element_ssid = ReadConfig_ACS_Tree.getSSID2()
            self.element_security = ReadConfig_ACS_Tree.getSSIDPwd6()
            self.SSID_Pwd = Input_File.SSID_Pwd_AP6[0]
        return self.element_ap, self.element_ssid, self.element_security, self.SSID_Pwd

    def GPV_SSIDName(self):
        element = self.driver.find_element(By.XPATH, self.textbox_SSID_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        Acs_SSIDName = self.driver.find_element(By.XPATH, self.textbox_SSID_xpath).get_attribute('value')
        return Acs_SSIDName

    def SSID_Name(self, SSID_number):
        SSID = ''
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        if SSID_number == 1:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID1())
            SSID = Input_File.SSID_AP1[0]
        elif SSID_number == 2:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID2())
            SSID = Input_File.SSID_AP2[0]
        elif SSID_number == 3:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID3())
            SSID = Input_File.SSID_AP3[0]
        elif SSID_number == 4:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID4())
            SSID = Input_File.SSID_AP4[0]
        elif SSID_number == 5:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID5())
            SSID = Input_File.SSID_AP5[0]
        elif SSID_number == 6:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSID6())
            SSID = Input_File.SSID_AP6[0]

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_edit_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, self.textbox_SSID_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH, self.textbox_SSID_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_SSID_xpath).send_keys(SSID)
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_sendUpdate_xpath).click()
        time.sleep(2)

        # alert = self.driver.switch_to.alert
        # alert.accept()
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_Alert_xpath).click()

        time.sleep(2)
        # self.driver.switch_to.default_content()
        # time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_alert_xpath).click()

    def SSID_Security(self, SSID_number):
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        SSID_Pwd = ''
        if SSID_number == 1:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd1())
            SSID_Pwd = Input_File.SSID_Pwd_AP1[0]
        elif SSID_number == 2:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd2())
            SSID_Pwd = Input_File.SSID_Pwd_AP2[0]
        elif SSID_number == 3:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd3())
            SSID_Pwd = Input_File.SSID_Pwd_AP3[0]
        elif SSID_number == 4:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd4())
            SSID_Pwd = Input_File.SSID_Pwd_AP4[0]
        elif SSID_number == 5:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd5())
            SSID_Pwd = Input_File.SSID_Pwd_AP5[0]
        elif SSID_number == 6:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getSSIDPwd6())
            SSID_Pwd = Input_File.SSID_Pwd_AP6[0]

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_edit_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, self.textbox_Security_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH, self.textbox_Security_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_Security_xpath).send_keys(SSID_Pwd)
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_sendUpdate_xpath).click()
        # alert = self.driver.switch_to.alert
        # alert.accept()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_Alert_xpath).click()
        time.sleep(2)
        # self.driver.switch_to.default_content()
        # time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_alert_xpath).click()

    def Check_AP_Status(self, SSID_number):
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        if SSID_number == 1:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp1())
        elif SSID_number == 2:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp2())
        elif SSID_number == 3:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp3())
        elif SSID_number == 4:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp4())
        elif SSID_number == 5:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp5())
        elif SSID_number == 6:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp6())

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, self.textbox_ApStatus_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        ApStatus = self.driver.find_element(By.XPATH, self.textbox_ApStatus_xpath).get_attribute('value')
        print(ApStatus)
        return ApStatus

    def Enable_AP(self, SSID_number):
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        if SSID_number == 1:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp1())
        elif SSID_number == 2:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp2())
        elif SSID_number == 3:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp3())
        elif SSID_number == 4:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp4())
        elif SSID_number == 5:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp5())
        elif SSID_number == 6:
            self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(
                ReadConfig_ACS_Tree.getAp6())

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_edit_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, self.textbox_ApStatus_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH, self.textbox_ApEnable_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_ApEnable_xpath).send_keys('1')
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_sendUpdate_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_Alert_xpath).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_alert_xpath).click()
        print('AP enabled successfully')

    def Check_SSIDBroadcast(self, SSID_number):
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        element1, element2, element3, element4 = acsWifi.Get_ElementId(self, SSID_number)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(element1)

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, self.textbox_SSIDBroadcast_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        BroadcastStatus = self.driver.find_element(By.XPATH, self.textbox_SSIDBroadcast_xpath).get_attribute('value')
        print('SSID Broadcast Status : ' + str(BroadcastStatus))
        return BroadcastStatus

    def Change_SSIDBroadcast(self, SSID_number, BroadcastChangeTo):
        time.sleep(10)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).clear()
        print('Checking SSID number ' + str(SSID_number))
        element1, element2, element3, element4 = acsWifi.Get_ElementId(self, SSID_number)
        self.driver.find_element(By.XPATH, self.textbox_deviceTreeSearch_xpath).send_keys(element1)

        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_edit_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmDesktop')
        time.sleep(2)

        element = self.driver.find_element(By.XPATH, self.textbox_SSIDBroadcast_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        self.driver.find_element(By.XPATH, self.textbox_SSIDBroadcast_xpath).clear()
        self.driver.find_element(By.XPATH, self.textbox_SSIDBroadcast_xpath).send_keys(BroadcastChangeTo)
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame('frmButtons')
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_sendUpdate_xpath).click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_Alert_xpath).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.button_alert_xpath).click()
