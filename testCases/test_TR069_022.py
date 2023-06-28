import pytest

from testCases.PacketAnalysis import Packet_read_ssid
from pageObjects.ArcGui_LoginPage import Login_GUI
from pageObjects.ArcGui_Wireless import Navigate_WiFi
from testCases import Input_File
from utilities.commonmethod import commonmethod
import time
from datetime import datetime
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from utilities.ReadAcsTree import ReadConfig_ACS_Tree


@pytest.mark.order(5)
class Test_TR069_024:
    #ReadConfig_ACS_Tree.setSSID(5)
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    logger = LogGen.loggen()

    def test_check_SSIDName_GUI(self, setup):
        ReadConfig_ACS_Tree.setSSID(5)
        Packet_Analysis_Result, acs_set_value = Packet_read_ssid.check_packet()
        print('Packet analysis result : ' + str(Packet_Analysis_Result))
        print('ACS SSID SPV result : ' + str(acs_set_value))
        self.logger.info('Test Login TO Device GUI')
        self.logger.info('Login to Device GUI')
        if acs_set_value == 'PASS':
            SSID_num = ReadConfig_ACS_Tree.getSSID()
            print('SSID_num = ' + str(SSID_num))
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
            GUI_SSID, GUI_Pwd = self.gw.SelectSubMenuGuestWiFi(SSID_number=SSID_num)
            time.sleep(10)
            self.driver.close()

            adb_result = commonmethod.connectWifiAndroid11(ssid=Input_File.SSID_AP5[0], password=GUI_Pwd,
                                                           security='wpa2', r=0)
            print('adb result' + adb_result)

            if GUI_SSID == Input_File.SSID_AP5[0] and Packet_Analysis_Result == 'PASS' and adb_result == 'Connected':
                result = 'PASS'
            else:
                result = 'FAIL'
        else:
            result = 'FAIL'
        assert result == 'PASS'
