import pytest
from pageObjects.ArcGui_LoginPage import Login_GUI
from pageObjects.ArcGui_Tr069Page import ChangeTr069Parameters
import time
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from testCases.conftest import setup


class Test_ChangeACSURL:
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    defaultPassword = ReadConfig_GUI_Environment.getDefaultPassword()
    logger = LogGen.loggen()

    def test_changeAcsUrl(self, setup, request):
        result = ''
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = Login_GUI(self.driver)
        self.lp.SetUserName(self.username)
        self.lp.SetPassword(self.password)
        self.lp.ClickLogin()
        time.sleep(5)
        try:
            self.lp.login_exception()
            time.sleep(10)
        except Exception as msg:
            print('No exception occurred during login')

        act_title = self.driver.title
        print('Title of page : ' + act_title)
        if act_title == 'Jio':
            print('Login successfully')
            URL = 'http://192.168.29.1/tr69.htm'
            self.driver.get(URL)
            time.sleep(10)
            self.TR = ChangeTr069Parameters(self.driver)
            self.TR.ChangeAcsUrl()
            self.TR.ChangeAcsUsername()
            self.TR.ChangeAcsPassword()
            time.sleep(1)
            self.TR.SaveAcsSettings()
            time.sleep(15)
            self.TR.ChangePeriodicTime()
            self.TR.SaveAcsSettings()
            time.sleep(15)
            result = 'Done'
        request.config._test_results[request.node.nodeid] = result
        print('result : ' + result)
        self.driver.close()




