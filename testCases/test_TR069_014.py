import pytest
from pageObjects.ACS_AdvancedView import Advanced_View
from pageObjects.ACS_Login import Login_ACS
from pageObjects.ACS_WiFi import acsWifi
from testCases.PacketAnalysis import Packet_read_ssidPwd
from pageObjects.ArcGui_LoginPage import Login_GUI
from pageObjects.ArcGui_Wireless import Navigate_WiFi
from testCases import Input_File
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from utilities.commonmethod import commonmethod
import time
from datetime import datetime
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from utilities.ReadAcsTree import ReadConfig_ACS_Tree


#@pytest.mark.order(7)
class Test_TR069_014:
    #ReadConfig_ACS_Tree.setSSID(1)
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    baseURL_acs = ReadConfig_ACS_Environment.getACSUrL()
    username_acs = ReadConfig_ACS_Environment.getUsername()
    password_acs = ReadConfig_ACS_Environment.getPassword()
    logger = LogGen.loggen()

    def test_tr069_014(self, setup):
        ReadConfig_ACS_Tree.setSSID(4)
        SSID_num = ReadConfig_ACS_Tree.getSSID()
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = Login_GUI(self.driver)
        self.lp.SetUserName(self.username)
        self.lp.SetPassword(self.password)
        self.lp.ClickLogin()
        time.sleep(5)
        try:
            self.lp.login_exception()
        except Exception as msg:
            print('No exception occurred during login')
        self.gw = Navigate_WiFi(self.driver)
        self.gw.SelectMenuWiFi()
        time.sleep(5)
        var = self.gw.GetBandSteeringStatus()
        if var == 1:
            self.gw.DisableBandSteering()
            time.sleep(10)

        self.lp.SwitchToDefault()
        SSIDName, SSIDPwd = self.gw.SetSSIDFromGui(SSID_num)
        print('SSID name on GUI: ' + str(SSIDName))

        time.sleep(5)

        self.driver.get(self.baseURL_acs)
        self.lp = Login_ACS(self.driver)
        self.lp.SetUserName(self.username_acs)
        self.lp.SetPassword(self.password_acs)
        self.lp.ClickLogin()
        time.sleep(5)
        self.lp.SearchDevice()
        self.Av = Advanced_View(self.driver)
        self.Av.SwitchToDefault()
        self.lp.DeviceInfo()

        self.Av.ClickAdvancedView()
        self.Av.SearchTreeElement('Device.WiFi.SSID.4')
        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmButtons')
        self.lp.GetCurrentParameter()
        time.sleep(10)
        self.Av.SwitchToDefault()
        self.lp.AcceptAlert2()
        time.sleep(40)
        self.Av.SwitchFrame('frmDesktop')
        self.Aw = acsWifi(self.driver)
        SSID_Acs = self.Aw.GPV_SSIDName()
        print('SSID name on ACS : ' + str(SSID_Acs))
        self.driver.close()

        if str(SSIDName) == str(SSID_Acs):
            result = 'PASS'
        else:
            result = 'FAIL'

        assert result == 'PASS'






