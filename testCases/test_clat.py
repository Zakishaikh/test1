import pytest
import scp
import paramiko
import time
import subprocess
from utilities.readProperties import ReadConfig_SSH_Environment_Arc_IDCPE, ReadConfig_SSH_Environment_Zyxel_IDU
from pageObjects.Read_Pcap_File import Packet_read
from utilities.customLogger import LogGen
from testCases import Input_File


class Test_clat_verification:
    logger = LogGen.loggen()

    @staticmethod
    def ping_Ipv4():
        command = 'cmd/c ping -4 google.com'
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = cmd.communicate()

    @staticmethod
    def SSH_Details():
        Device_Type = Input_File.Device_Type
        print('Test is running on : ' + Device_Type)
        if Device_Type == 'Arcadyan_IDCPE':
            command1 = 'tcpdump -b -s 1600 -ni ccmni2 -w wan.pcap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Arc_IDCPE.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHPassword()
            Test_clat_verification.logger.info('Router Ip : ' + router_ip)
            Test_clat_verification.logger.info('Router SSH Username : ' + router_username)
            Test_clat_verification.logger.info('Router SSH Password : ' + router_password)
        elif Device_Type == 'Zyxel_IDU':
            command1 = '/usr/sbin/tcpdump -b -s 1600 -ni eth1.2 -w wan.pcap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Zyxel_IDU.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHPassword()
            Test_clat_verification.logger.info('Router Ip : ' + router_ip)
            Test_clat_verification.logger.info('Router SSH Username : ' + router_username)
            Test_clat_verification.logger.info('Router SSH Password : ' + router_password)
        return command1, router_ip, router_username, router_password

    @staticmethod
    def test_clat_functionality():
        command1, router_ip, router_username, router_password = Test_clat_verification.SSH_Details()

        file_name = Packet_read.file_name

        command2 = 'killall -9 tcpdump'
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)

        time.sleep(10)

        Test_clat_verification.ping_Ipv4()

        time.sleep(60)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)

        s = scp.SCPClient(ssh.get_transport())

        s.get('wan.pcap', file_name)

        error = ssh_stderr.readlines()
        output = ssh_stdout.readlines()
        ssh.close()

        result = Packet_read.compare_pcap()
        if result == 'PASS':
            assert True
        else:
            assert False
