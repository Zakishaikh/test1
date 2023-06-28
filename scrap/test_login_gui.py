import time
from pageObjects.ArcGui_LoginPage import Login_GUI
from datetime import datetime
from utilities.readProperties import ReadConfig_GUI_Environment
from utilities.customLogger import LogGen


class Test_loginDeviceGUI:
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    logger = LogGen.loggen()

    def test_homePageTitle(self, setup):
        self.logger.info('Test Login TO Device GUI')
        self.logger.info('Login to Device GUI')
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = Login_GUI(self.driver)
        self.lp.SetUserName(self.username)
        self.lp.SetPassword(self.password)
        self.lp.ClickLogin()
        time.sleep(30)
        act_title = self.driver.title
        self.logger.info('Verifying Home Page Title')
        if act_title == 'Jio':
            print('testcase pass')
            self.logger.info('Login test is passed')
            self.driver.close()
            assert True
        else:
            print('testcase fail')
            self.logger.error('Login test is failed')
            current_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
            print(current_time)
            self.driver.save_screenshot('.\\Screenshots\\' + 'test_homePageTitle_' + current_time + '.png')
            self.driver.close()
            assert False
