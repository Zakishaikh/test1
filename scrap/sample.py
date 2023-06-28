import scp
import paramiko
import time
from pageObjects.Read_Pcap_File import Packet_read

router_ip = '192.168.31.1'
router_username = 'admin'
router_password = 'Jiocentrum'
file_name = Packet_read.file_name
# command1 = 'tcpdump -b -s 1600 -ni ccmni2 -w wan.pcap -C 20 -W 1'
command1 = 'tcpdump -b -s 1600 -ni br0 -w wan.pcap -C 20 -W 1'
command2 = 'killall tcpdump'
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

s.get('wan.pcap', file_name)
