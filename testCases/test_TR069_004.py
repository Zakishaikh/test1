import time
import pytest
from datetime import datetime
from pageObjects.ACS_Login import Login_ACS
from pageObjects.ACS_AdvancedView import Advanced_View
from pageObjects.ACS_DeviceHistory import deviceHistory
from pageObjects.ArcGui_Wireless import Navigate_WiFi
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from utilities.readProperties import ReadConfig_GUI_Environment
from pageObjects.ArcGui_Dashboard import Navigate_Overview
from pageObjects.ArcGui_LoginPage import Login_GUI
from utilities.commonmethod import commonmethod
from testCases.conftest import setup
import datetime


# @pytest.mark.order()
#@pytest.mark.repeat(5)
class Test_RebootDut:
    baseURL_acs = ReadConfig_ACS_Environment.getACSUrL()
    username_acs = ReadConfig_ACS_Environment.getUsername()
    password_acs = ReadConfig_ACS_Environment.getPassword()
    baseURL_GUI = ReadConfig_GUI_Environment.getGatewayUrL()
    username_GUI = ReadConfig_GUI_Environment.getUsername()
    password_GUI = ReadConfig_GUI_Environment.getPassword()

    def test_rebootDevice(self, setup):
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
        self.lp.Reboot()
        self.Av.SwitchToDefault()
        time.sleep(2)
        self.lp.AcceptAlert1()
        time.sleep(2)
        # self.driver.close()

        time.sleep(300)

        currentDate, currentTime = commonmethod.FindCurrentTime()
        print('current date : ' + str(currentDate))
        print('current time in sec: ' + str(currentTime))

        self.driver.get(self.baseURL_GUI)
        self.lui = Login_GUI(self.driver)
        self.lui.SetUserName(self.username_GUI)
        self.lui.SetPassword(self.password_GUI)
        self.lui.ClickLogin()
        time.sleep(5)
        try:
            self.lui.login_exception()
            time.sleep(10)
        except Exception as msg:
            print('No exception occurred during login')

        act_title = self.driver.title
        print('Title of page : ' + act_title)
        if act_title == 'Jio':
            print('Login successfully')
            self.db = Navigate_Overview(self.driver)
            self.db.SelectMenuOverview()
            self.db.SelectSubMenu_RouterInformation()
            time.sleep(2)
            self.lui.SwitchFrame('frm_main2')
            time.sleep(2)
            systemUptime = self.db.CheckDeviceUptime()
            print('System Uptime on Device GUI : ' + str(systemUptime))
            a = systemUptime.split(' ')
            if 'day(s)' in a:
                index_day = a.index('day(s)')
                up_day = a[index_day - 1]
            else:
                up_day = 0

            if 'hour(s)' in a:
                index_hr = a.index('hour(s)')
                up_hr = a[index_hr - 1]
            else:
                up_hr = 0

            if 'minute(s)' in a:
                index_min = a.index('minute(s)')
                up_min = a[index_min - 1]
            else:
                up_min = 0

            if 'second(s)' in a:
                index_sec = a.index('second(s)')
                up_sec = a[index_sec - 1]
            else:
                up_sec = 0

            DutUptime = int(up_day) * 86400 + int(up_hr) * 3600 + int(up_min) * 60 + int(up_sec)
            print('System Uptime on Device GUI in Secs: ' + str(DutUptime))

        self.lui.SwitchToDefault()
        self.ov = Navigate_Overview(self.driver)
        self.ov.SelectMenuOverview()
        self.ov.SelectSubMenu_NetworkStatus()
        broadcastStatus = self.ov.GetBroadcastStatus(1)
        print('AP Broadcast status on GUI : ' + str(broadcastStatus))
        self.lui.SwitchToDefault()
        self.gw = Navigate_WiFi(self.driver)
        self.gw.SelectMenuWiFi()
        time.sleep(5)
        SSID_name = self.gw.SelectSubMenuWireless(SSID_number=1)
        print('SSID name on GUI : ' + SSID_name)
        SSID_pwd = self.gw.CheckSsidPwd(SSID_number=1)
        print('SSID pwd onn GUI : ' + SSID_pwd)


        time.sleep(10)
        self.driver.get(self.baseURL_acs)
        self.lp.SetUserName(self.username_acs)
        self.lp.SetPassword(self.password_acs)
        self.lp.ClickLogin()
        time.sleep(5)
        self.lp.SearchDevice()
        self.Av = Advanced_View(self.driver)
        self.Av.SwitchToDefault()
        self.lp.DeviceInfo()
        time.sleep(2)
        self.Dh = deviceHistory(self.driver)
        self.Dh.ClickDeviceHistory()
        self.Av.SwitchFrame('frmDesktop')
        self.Dh.SelectEvent('M Reboot')
        time.sleep(5)
        EventTimestamp = self.Dh.GetEventGeneratedTime()

        acs_date, acs_time = commonmethod.TimeConversion(EventTimestamp)
        print('M reboot date: ' + str(acs_date))
        print('M reboot time in sec: ' + str(acs_time))

        self.driver.close()

        adb_result = commonmethod.connectWifiAndroid11(ssid=SSID_name, password=SSID_pwd, security='wpa2', r=0)

        if str(currentDate).strip() == str(acs_date).strip() and int(currentTime) - int(
                acs_time) <= 200 and int(DutUptime) <= 300 and adb_result == 'Connected':
            result = 'PASS'
            print('PASS')
        else:
            result = 'FAIL'
            print('FAIL')

        assert result == 'PASS'
