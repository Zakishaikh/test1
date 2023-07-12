import time
from pageObjects.ACS_Login import Login_ACS
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from pageObjects.ACS_AdvancedView import Advanced_View
from pageObjects.ACS_Ethernet import EthernetStats
from pageObjects.ACS_WiFi import acsWifi
from pageObjects.ACS_Tasks import AcsTasks
from utilities.ReadAcsTree import ReadConfig_ACS_Tree
from testCases import Input_File
from testCases.conftest import setup


class Test_CheckEthernetStats:
    baseURL_acs = ReadConfig_ACS_Environment.getACSUrL()
    username_acs = ReadConfig_ACS_Environment.getUsername()
    password_acs = ReadConfig_ACS_Environment.getPassword()
    youtube_url = 'https://www.youtube.com/watch?v=uh0qO-sLbRw'

    def test_check_ethStats(self, setup):
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
        self.lp.DeviceInfo()

        self.Av.ClickAdvancedView()
        time.sleep(5)
        self.Av.SearchTreeElement(ReadConfig_ACS_Tree.getInterface1Stats())
        time.sleep(2)

        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmButtons')
        self.lp.GetCurrentParameter()
        time.sleep(10)
        self.Av.SwitchToDefault()
        self.lp.AcceptAlert2()
        time.sleep(30)

        self.Es = EthernetStats(self.driver)
        self.Av.SwitchFrame('frmDesktop')
        BytesReceived_before = self.Es.GetBytesReceived_Stats()
        print('Bytes Received before playing youtube video : ' + str(BytesReceived_before))
        BytesSent_before = self.Es.GetBytesSent_Stats()
        print('Bytes Sent before playing youtube video : ' + str(BytesSent_before))
        PacketsReceived_before = self.Es.GetPacketsReceived_Stats()
        print('Packets Received before playing youtube video : ' + str(PacketsReceived_before))
        PacketsSent_before = self.Es.GetPacketsSent_Stats()
        print('Packets Sent before playing youtube video : ' + str(PacketsSent_before))

        self.driver.get(self.youtube_url)
        time.sleep(60)

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
        time.sleep(5)
        self.Av.SearchTreeElement(ReadConfig_ACS_Tree.getInterface1Stats())
        time.sleep(2)

        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmButtons')
        self.lp.GetCurrentParameter()
        time.sleep(10)
        self.Av.SwitchToDefault()
        self.lp.AcceptAlert2()
        time.sleep(30)

        self.Es = EthernetStats(self.driver)
        self.Av.SwitchFrame('frmDesktop')
        BytesReceived_after = self.Es.GetBytesReceived_Stats()
        print('Bytes Received after playing youtube video : ' + str(BytesReceived_after))
        BytesSent_after = self.Es.GetBytesSent_Stats()
        print('Bytes Sent after playing youtube video : ' + str(BytesSent_after))
        PacketsReceived_after = self.Es.GetPacketsReceived_Stats()
        print('Packets Received after playing youtube video : ' + str(PacketsReceived_after))
        PacketsSent_after = self.Es.GetPacketsSent_Stats()
        print('Packets Sent after playing youtube video : ' + str(PacketsSent_after))

        self.driver.close()

        if BytesReceived_before < BytesReceived_after and BytesSent_before < BytesSent_after and PacketsReceived_before < PacketsReceived_after and PacketsSent_before < PacketsSent_after:
            result = 'PASS'
        else:
            result = 'FAIL'

        assert result == 'PASS'







