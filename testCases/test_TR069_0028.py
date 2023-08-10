import pytest

from testCases.PacketAnalysis import Packet_read_ssidBroadcast
from pageObjects.ArcGui_LoginPage import Login_GUI
from pageObjects.ArcGui_Wireless import Navigate_WiFi
from pageObjects.ArcGui_Dashboard import Navigate_Overview
from testCases import Input_File
from utilities.commonmethod import commonmethod
import time
from datetime import datetime
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig_GUI_Environment
from utilities.ReadAcsTree import ReadConfig_ACS_Tree


@pytest.mark.order(17)
@pytest.mark.repeat(2)
class Test_TR069_changeBroadcast:
    #ReadConfig_ACS_Tree.setSSID(5)
    baseURL = ReadConfig_GUI_Environment.getGatewayUrL()
    username = ReadConfig_GUI_Environment.getUsername()
    password = ReadConfig_GUI_Environment.getPassword()
    logger = LogGen.loggen()

    def test_check_Broadcast_GUI(self, setup):
        ReadConfig_ACS_Tree.setSSID(5)
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

        global broadcastStatus, SSID_pwd, SSID_name, adb_status

        Packet_Analysis_Result, acs_set_value, broadcastValue = Packet_read_ssidBroadcast.check_packet()
        if int(broadcastValue) == 1:
            BroadcastValue = 'Enable'
        elif int(broadcastValue) == 0:
            BroadcastValue = 'Disable'
        print('BroadcastValue received from acs : ' + str(BroadcastValue))
        print('Packet analysis result : ' + str(Packet_Analysis_Result))
        print('ACS SSID SPV result : ' + str(acs_set_value))
        self.logger.info('Test Login TO Device GUI')
        self.logger.info('Login to Device GUI')
        if acs_set_value == 'PASS':
            try:
                self.lp.SwitchToDefault()
                self.ov = Navigate_Overview(self.driver)
                self.ov.SelectMenuOverview()
                self.ov.SelectSubMenu_NetworkStatus()
                broadcastStatus = self.ov.GetBroadcastStatus(int(SSID_num))
                print('AP Broadcast status on GUI : ' + str(broadcastStatus))
                self.lp.SwitchToDefault()
                self.gw = Navigate_WiFi(self.driver)
                self.gw.SelectMenuWiFi()
                time.sleep(5)
                SSID_name, SSID_pwd = self.gw.SelectSubMenuGuestWiFi(SSID_number=SSID_num)
                print('SSID name on GUI : ' + SSID_name)
                print('SSID pwd on GUI : ' + SSID_pwd)
            except Exception as msg:
                print('Exception occurred')

            try:
                self.lp.SetUserName(self.username)
                self.lp.SetPassword(self.password)
                self.lp.ClickLogin()
                time.sleep(5)
                try:
                    self.lp.login_exception()
                except Exception as msg:
                    print('No exception occurred during login')
                self.ov = Navigate_Overview(self.driver)
                self.ov.SelectMenuOverview()
                self.ov.SelectSubMenu_NetworkStatus()
                broadcastStatus = self.ov.GetBroadcastStatus(int(SSID_num))
                print('AP5 Broadcast status on GUI : ' + str(broadcastStatus))
                self.lp.SwitchToDefault()
                self.gw = Navigate_WiFi(self.driver)
                self.gw.SelectMenuWiFi()
                time.sleep(5)
                SSID_name, SSID_pwd = self.gw.SelectSubMenuGuestWiFi(SSID_number=SSID_num)
                print('SSID name on GUI : ' + SSID_name)
                print('SSID pwd on GUI : ' + SSID_pwd)

            except Exception as msg:
                print('Exception occurred')
        self.driver.close()

        adb_result = commonmethod.connectWifiAndroid11(ssid=SSID_name, password=SSID_pwd, security='wpa2', r=0)
        print('adb result : ' + adb_result)
        if int(broadcastValue) == 1:
            adb_status = 'Connected'
        elif int(broadcastValue) == 0:
            adb_status = 'FAIL'

        if str(broadcastStatus) == str(
                BroadcastValue) and Packet_Analysis_Result == 'PASS' and adb_result == adb_status:
            result = 'PASS'
        else:
            result = 'FAIL'
        assert result == 'PASS'
        time.sleep(60)
