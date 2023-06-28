import paramiko
from utilities.readProperties import ReadConfig_SSH_Environment_Zyxel_IDU, ReadConfig_SSH_Environment_Arc_IDCPE
from testCases import Input_File


class find_prefix:

    @staticmethod
    def SSH_Info():
        Device_Type = Input_File.Device_Type
        if Device_Type == 'Arcadyan_IDCPE':
            command = 'ifconfig ccmni2 | grep Global'
            router_ip = ReadConfig_SSH_Environment_Arc_IDCPE.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Arc_IDCPE.getSSHPassword()
            prefix_len = '/128'
        elif Device_Type == 'Zyxel_IDU':
            command = '/sbin/ifconfig eth1.2 | grep Global'
            router_ip = ReadConfig_SSH_Environment_Zyxel_IDU.getGatewayIp()
            router_username = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHUsename()
            router_password = ReadConfig_SSH_Environment_Zyxel_IDU.getSSHPassword()
            prefix_len = '/64'
        return command, router_ip, router_username, router_password, prefix_len

    @staticmethod
    def IPv6_Prefix():
        Device_Type = Input_File.Device_Type
        command, router_ip, router_username, router_password, prefix_len = find_prefix.SSH_Info()

        ssh = paramiko.SSHClient()

        # Load SSH host keys.
        ssh.load_system_host_keys()
        # Add SSH host key automatically if needed.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to router using username/password authentication.
        ssh.connect(router_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)
        # Run command.
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

        output = ssh_stdout.readlines()
        # Close connection.
        ssh.close()

        f = open("output.txt", "w")
        f.write(str(output))
        f.close()

        with open("output.txt", 'r') as fp:
            line = str(fp.readlines())
            line = line.split(':')
            if Device_Type == 'Arcadyan_IDCPE':
                prefix = line[1] + ':' + line[2] + ':' + line[3] + ':' + line[4]
                print('Prefix received from Device : ' + prefix)
            elif Device_Type == 'Zyxel_IDU':
                prefix = line[1] + ':' + line[2] + ':' + line[3] + ':' + line[4] + ':8000:0'
                print('Prefix received from Device : ' + prefix)

        return prefix

        # Analyze show ip route output
        # for line in output:
        #     if prefix_len in line:
                # index1 = line.index('addr:')
                # print(index1)
                # index2 = line.index(prefix_len)
                # print(index2)
                # prefix = line[index1 + 5:index2 - 7]
                # print(prefix)
                #return prefix



