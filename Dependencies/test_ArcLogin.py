import pytest
from pageObjects.ArcGui_LoginPage import Login_GUI
import time
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from testCases.conftest import setup


class Test_LoginGui:
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    defaultPassword = ReadConfig_GUI_Environment.getDefaultPassword()
    logger = LogGen.loggen()

    def test_loginGui(self, setup, request):
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
        else:
            print('Need to Login with default password')
            self.lp.SetUserName(self.username)
            self.lp.SetPassword(self.defaultPassword)
            self.lp.ClickLogin()
            time.sleep(5)

            self.lp.ChangeGUIPwd(self.password)
            time.sleep(10)
            print('Device is in factory reset condition, Setting new Login password')

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

                result = 'FactoryDone'

                request.config._test_results[request.node.nodeid] = result
        print('result : ' + result)
        self.driver.close()
