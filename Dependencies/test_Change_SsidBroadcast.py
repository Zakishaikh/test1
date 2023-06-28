import time
from pageObjects.ACS_Login import Login_ACS
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from pageObjects.ACS_AdvancedView import Advanced_View
from pageObjects.ACS_WiFi import Set_SsidName
from pageObjects.ACS_Tasks import AcsTasks
from utilities.ReadAcsTree import ReadConfig_ACS_Tree
from testCases import Input_File
from testCases.conftest import setup


class Test_ChangeSsidBroadcast:
    baseURL_acs = ReadConfig_ACS_Environment.getACSUrL()
    username_acs = ReadConfig_ACS_Environment.getUsername()
    password_acs = ReadConfig_ACS_Environment.getPassword()

    def test_change_SSIDBroadcast_ACS(self, setup, request):
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

        self.At = AcsTasks(self.driver)
        CompletedTask_before = self.At.CompletedTask()
        RejectedTask_before = self.At.RejectedTask()
        FailedTask_before = self.At.FailedTask()

        self.Av.ClickAdvancedView()
        self.Ss = Set_SsidName(self.driver)
        SSID_number = ReadConfig_ACS_Tree.getSSID()
        ApStatus = self.Ss.Check_AP_Status(SSID_number=int(SSID_number))
        print('Ap Status : ' + str(ApStatus))

        if int(ApStatus) == 0:
            print('AP is Disabled')
            print('Enabling AP')
            self.Av.SwitchToDefault()
            self.Av.SwitchFrame('frmDesktop')
            self.Ss.Enable_AP(SSID_number=int(SSID_number))
        else:
            print('AP is enabled')

        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmDesktop')
        BroadcastStatus = self.Ss.Check_SSIDBroadcast(SSID_number=int(SSID_number))

        if int(BroadcastStatus) == 1:
            statement = 'SSID broadcast disabled successfully'
            print('SSID broadcast is enabled, now Disabling broadcast')
            broadcast_changedTo = 0
        else:
            statement = 'SSID broadcast enabled successfully'
            print('SSID broadcast is disabled, now enabling broadcast')
            broadcast_changedTo = 1

        self.Av.SwitchToDefault()
        self.Av.SwitchFrame('frmDesktop')
        self.Ss.Change_SSIDBroadcast(int(SSID_number), int(broadcast_changedTo))
        time.sleep(10)

        self.Av.SwitchToDefault()
        PendingTask = self.At.PendingTask()
        SentTask = self.At.SentTask()
        CompletedTask_after = self.At.CompletedTask()
        RejectedTask_after = self.At.RejectedTask()
        FailedTask_after = self.At.FailedTask()

        counter = 0
        if CompletedTask_before < CompletedTask_after:
            print('Completed task count increased , Rejected TAsk and Failed task count remain same')
            counter = counter + 1
        if RejectedTask_before == RejectedTask_after:
            print('Rejected Task remain same')
            counter = counter + 1

        if FailedTask_before == FailedTask_after:
            print('Failed Task count remain same')
            counter = counter + 1

        if PendingTask == SentTask == '0':
            print('No tasks in Pending and Sent task list')
            counter = counter + 1

        print('counter ===> ' + str(counter))
        if counter == 4:
            ACS_Result = 'PASS'
            print(statement)
        else:
            i = 0
            count = 0
            ACS_Result = 'FAIL'
            while i != 5:
                time.sleep(30)
                PendingTask = self.At.PendingTask()
                SentTask = self.At.SentTask()
                CompletedTask_after = self.At.CompletedTask()
                RejectedTask_after = self.At.RejectedTask()
                FailedTask_after = self.At.FailedTask()

                if CompletedTask_before < CompletedTask_after:
                    print('Completed task count increased , Rejected TAsk and Failed task count remain same')
                    count = count + 1
                if RejectedTask_before == RejectedTask_after:
                    print('Rejected Task remain same')
                    count = count + 1

                if FailedTask_before == FailedTask_after:
                    print('Failed Task count remain same')
                    count = count + 1

                if PendingTask == SentTask == '0':
                    print('No tasks in Pending and Sent task list')
                    count = count + 1

                if count == 4:
                    ACS_Result = 'PASS'
                    print(statement)
                    break
                else:
                    print('Checking Task list again')
                    count = 0
                i = i + 1
            # print('count ===> ' + str(count))
        request.config._test_results[request.node.nodeid] = ACS_Result, broadcast_changedTo
        self.driver.close()
        time.sleep(60)
