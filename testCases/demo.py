import paramiko
import time



def SSH_Details():
    router_ip = '192.168.29.1'
    router_username = 'root'
    router_password = 'Jiocentrum'
    command = 'ifconfig'
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
    print('waiting')
    time.sleep(60)

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


