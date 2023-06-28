import time
from pageObjects.ArcGui_LoginPage import Login_GUI
from datetime import datetime
from utilities.readProperties import ReadConfig_GUI_Environment
from testCases.conftest import setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class loginDeviceGUI:
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    ser = Service(".\\chromedriver.exe")
    op = webdriver.ChromeOptions()
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    op.add_argument('--ignore-certificate-errors-spki-list')
    op.add_argument('--ignore-ssl-errors')
    op.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(service=ser, options=op)

    @staticmethod
    def homePageTitle():
        driver = loginDeviceGUI.driver
        driver.maximize_window()
        driver.get(loginDeviceGUI.baseURL)
        lp = Login_GUI(driver)
        lp.SetUserName(loginDeviceGUI.username)
        lp.SetPassword(loginDeviceGUI.password)
        lp.ClickLogin()
        time.sleep(30)
        act_title = driver.title
        if act_title == 'Jio':
            print('GUI login successful')
            lp.Click_NetworkStatus()
            time.sleep(5)
            lp.Get_5G_Info()

            #driver.close()
        else:
            print('GUI login failed')
            current_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
            print(current_time)
            driver.save_screenshot('.\\Screenshots\\' + 'test_homePageTitle_' + current_time + '.png')
            #driver.close()


loginDeviceGUI.homePageTitle()
