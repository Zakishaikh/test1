import pytest
from datetime import datetime
import scp
import paramiko
import time
import testCases
from utilities.readProperties import ReadConfig_SSH_Environment_Arc_IDCPE, ReadConfig_SSH_Environment_Zyxel_IDU
from utilities.customLogger import LogGen
from testCases import Input_File
from Dependencies.test_Change_SSID import Test_ChangeSsidName


class ResultCollector:

    def __int__(self):
        self.return_value = str

    def pytest_configure(self, config):
        config._test_results = dict()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        if report.when == 'call':
            self.return_value = item.config._test_results.get(item.nodeid, None)


class Ssh_To_DUT:
    logger = LogGen.loggen()

    file_name = '..\\PacketCapture\\testdump_' + str(datetime.now().strftime("%d%m%Y%H%M")) + '.pcap'

    @staticmethod
    def SSH_Details():
        Device_Type = Input_File.Device_Type
        command = 'ifconfig'

        if Device_Type == 'Arcadyan_IDCPE':
            router_ip = ReadConfig_SSH_Environment_Arc_IDCPE.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHPassword()
        elif Device_Type == 'Zyxel_IDU':
            router_ip = ReadConfig_SSH_Environment_Zyxel_IDU.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHPassword()

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        output = ssh_stdout.readlines()
        with open("backup.txt", "w") as out_file:
            for line in output:
                out_file.write(line)
        time.sleep(2)
        ssh.close()

        with open(r'backup.txt', 'r') as file:
            # read all content from a file using read()
            content = file.read()
            # check if string present or not
            if 'ccmni1' in content:
                interface_name = 'ccmni1'
            elif 'ccmni2' in content:
                interface_name = 'ccmni2'
            else:
                print('wan interface is down')
            print('interface name : ' + interface_name)

        print('Test is running on : ' + Device_Type)
        if Device_Type == 'Arcadyan_IDCPE':
            command1 = 'tcpdump -b -s 1600 -ni ' + interface_name + ' -w wan.pcap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Arc_IDCPE.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHPassword()
            Ssh_To_DUT.logger.info('Router Ip : ' + router_ip)
            Ssh_To_DUT.logger.info('Router SSH Username : ' + router_username)
            Ssh_To_DUT.logger.info('Router SSH Password : ' + router_password)
        elif Device_Type == 'Zyxel_IDU':
            command1 = '/usr/sbin/tcpdump -b -s 1600 -ni eth1.2 -w wan.pcap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Zyxel_IDU.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHPassword()
            Ssh_To_DUT.logger.info('Router Ip : ' + router_ip)
            Ssh_To_DUT.logger.info('Router SSH Username : ' + router_username)
            Ssh_To_DUT.logger.info('Router SSH Password : ' + router_password)
        return command1, router_ip, router_username, router_password

    @staticmethod
    def login_ssh_ssid():
        command1, router_ip, router_username, router_password = Ssh_To_DUT.SSH_Details()
        command2 = 'killall -9 tcpdump'
        file_name = Ssh_To_DUT.file_name

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)
        print('SSH done and Tcpdump started')

        time.sleep(10)
        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_Change_SSID.py'], plugins=[collector])
        acs_set_value = collector.return_value
        print('SSID changed from ACS status : ' + str(acs_set_value))

        if acs_set_value == 'PASS':
            print('SSID set successfully from ACS')
        else:
            print('SSID set from ACS failed')

        print('Waiting for 120sec')
        time.sleep(60)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)

        print('Tcpdump stopped')

        s = scp.SCPClient(ssh.get_transport())

        s.get('wan.pcap', file_name)

        error = ssh_stderr.readlines()
        output = ssh_stdout.readlines()
        ssh.close()
        return acs_set_value

    @staticmethod
    def login_ssh_ssidPwd():
        command1, router_ip, router_username, router_password = Ssh_To_DUT.SSH_Details()
        print(command1)
        command2 = 'killall -9 tcpdump'
        file_name = Ssh_To_DUT.file_name

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)
        print('SSH done and Tcpdump started')

        time.sleep(10)
        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_Change_SsidPwd.py'], plugins=[collector])
        acs_set_value = collector.return_value
        print('SSID Password changed from ACS status : ' + str(acs_set_value))

        if acs_set_value == 'PASS':
            print('SSID set successfully from ACS')
        else:
            print('SSID set from ACS failed')

        print('Waiting for 120sec')
        time.sleep(60)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)

        print('Tcpdump stopped')

        s = scp.SCPClient(ssh.get_transport())

        s.get('wan.pcap', file_name)

        error = ssh_stderr.readlines()
        output = ssh_stdout.readlines()
        ssh.close()
        return acs_set_value

    @staticmethod
    def login_ssh_ssidBroadcast():
        command1, router_ip, router_username, router_password = Ssh_To_DUT.SSH_Details()
        print(command1)
        command2 = 'killall -9 tcpdump'
        file_name = Ssh_To_DUT.file_name

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)
        print('SSH done and Tcpdump started')

        time.sleep(10)
        collector = ResultCollector()
        pytest.main(['--capture=tee-sys', '../Dependencies/test_Change_SsidBroadcast.py'], plugins=[collector])
        acs_set_value, broadcastValue = collector.return_value
        print('SSID Password changed from ACS status : ' + str(acs_set_value))

        if acs_set_value == 'PASS':
            print('SSID set successfully from ACS')
        else:
            print('SSID set from ACS failed')

        print('Waiting for 120sec')
        time.sleep(60)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)

        print('Tcpdump stopped')

        s = scp.SCPClient(ssh.get_transport())

        s.get('wan.pcap', file_name)

        error = ssh_stderr.readlines()
        output = ssh_stdout.readlines()
        ssh.close()
        return acs_set_value, broadcastValue
