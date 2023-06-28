from pageObjects.ArcGui_LoginPage import Login_GUI
import time
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from utilities import XLUtils

class Test_LoginGui:
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    path = '../TestData/testData_User.xlsx'
    logger = LogGen.loggen()

    def test_loginGui(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = Login_GUI(self.driver)
        self.rows = XLUtils.getRowCount(self.path, 'Sheet1')
        print('Number of rows : ' + str(self.rows))

        for r in range(2,self.rows+1):
            self.username = XLUtils.readData(self.path, 'Sheet1', r, 1)
            self.password = XLUtils.readData(self.path,'Sheet1', r, 2 )
            self.exp = XLUtils.readData(self.path, 'Sheet1', r, 3)
            self.lp.SetUserName(self.username)
            self.lp.SetPassword(self.password)
            self.lp.ClickLogin()
            time.sleep(5)
            try:
                self.lp.login_exception()
            except Exception as msg:
                print('No exception occurred during login')

            time.sleep(5)
            act_title = self.driver.title
            print('Title of page : ' + act_title)
            if act_title == 'Jio':
                self.status = 'PASS'
                print('Login successfully')
            else:
                self.status = 'FAIL'
                print('Login failed')

            if self.status == self.exp:
                print('Testcase Pass')
            else:
                print('Testcase failed')

            try:
                self.lp.ClickLogout()
                time.sleep(10)
            except Exception as msg:
                print('Exception occurred')

