import time

import paramiko
import scp

from utilities.readProperties import ReadConfig_SSH_Environment_Zyxel_IDU, ReadConfig_SSH_Environment_Arc_IDCPE
from testCases import Input_File


class find_prefix:

    @staticmethod
    def SSH_Info():
        Device_Type = Input_File.Device_Type
        if Device_Type == 'Arcadyan_IDCPE':
            command1 = 'tcpdump -b -s 1600 -ni ccmni2 -w wan.pcap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Arc_IDCPE.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHPassword()
        elif Device_Type == 'Zyxel_IDU':
            command1 = 'tcpdump -b -s 1600 -ni eth1.2 -w wan.cap -C 20 -W 1'
            router_ip = ReadConfig_SSH_Environment_Zyxel_IDU.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHPassword()
        return command1, router_ip, router_username, router_password

    @staticmethod
    def IPv6_Prefix():
        command1, router_ip, router_username, router_password = find_prefix.SSH_Info()
        command2 = 'killall -9 tcpdump'
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)

        time.sleep(60)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)

        s = scp.SCPClient(ssh.get_transport())

        s.get('wan.pcap', 'IDU.pcap')

        error = ssh_stderr.readlines()
        output = ssh_stdout.readlines()
        ssh.close()


find_prefix.IPv6_Prefix()