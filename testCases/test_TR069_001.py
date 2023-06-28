import time
import pytest
from datetime import datetime
from pageObjects.ACS_DeviceHistory import deviceHistory
from pageObjects.ACS_Login import Login_ACS
from pageObjects.ACS_AdvancedView import Advanced_View
from pageObjects.SSH_DUT import ResultCollector
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from utilities.commonmethod import commonmethod
from pageObjects.ArcGui_Dashboard import Navigate_Overview
from pageObjects.ArcGui_LoginPage import Login_GUI
from Dependencies.test_ChangeACSParameters import Test_ChangeACSURL
from utilities.ReadAcsTree import ReadConfig_ACS_Tree
from testCases.conftest import setup
from utilities.readProperties import ReadConfig_GUI_Environment


# @pytest.mark.order()
# @pytest.mark.repeat(5)
class Test_FactoryReset:
    baseURL_acs = ReadConfig_ACS_Environment.getACSUrL()
    username_acs = ReadConfig_ACS_Environment.getUsername()
    password_acs = ReadConfig_ACS_Environment.getPassword()
    baseURL_GUI = ReadConfig_GUI_Environment.getGatewayUrL()
    username_GUI = ReadConfig_GUI_Environment.getUsername()
    password_GUI = ReadConfig_GUI_Environment.getPassword()

    def test_factoryReset(self, setup, request):
        global DutUptime
        self.driver = setup
        self.driver.get(self.baseURL_acs)
        self.lp = Login_ACS(self.driver)
        self.lp.SetUserName(self.username_acs)
        self.lp.SetPassword(self.password_acs)
        self.lp.ClickLogin()
        time.sleep(5)
        self.lp.SearchDevice()
        self.Av = Advanced_View(self.driver)
        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmDesktop')
        time.sleep(5)
        self.lp.FactoryReset()
        self.Av.SwitchToDefault()
        time.sleep(2)
        self.lp.AcceptAlert1()
        time.sleep(2)
        self.driver.close()

        time.sleep(300)

        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_ArcLogin.py'], plugins=[collector])
        GUI_result = collector.return_value
        print('GUI result : ' + str(GUI_result))

        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_CheckAcsParameters.py'], plugins=[collector])
        acs_url, acs_user, acs_pwd = collector.return_value
        acs_act_url = 'https://acs.oss.jio.com:8443/ftacs-digest/ACS'
        acs_act_user = ReadConfig_ACS_Environment.getDeviceSerial()

        if str(acs_url) == str(acs_act_url) and str(acs_user) == str(acs_act_user) and str(acs_pwd) != 'Jdev_1214':
            result = 'PASS'
        else:
            result = 'FAIL'

        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_ChangeACSParameters.py'], plugins=[collector])
        AcsChanges = collector.return_value
        print('Acs Changes are  : ' + str(AcsChanges))

        assert result == 'PASS'
