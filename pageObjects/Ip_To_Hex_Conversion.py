import socket
import subprocess
from utilities.customLogger import LogGen
from pageObjects.Find_IPv6_Prefix import find_prefix
from testCases import Input_File


class IpToHex:
    logger = LogGen.loggen()

    @staticmethod
    def find_ip():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        #print("Client IPv4 Address : " + ip_address)
        IpToHex.logger.info('"Client IPv4 Address: {ip_address}"')
        return ip_address

    @staticmethod
    def client_ip():
        ip_address = IpToHex.find_ip()
        ip_address = ip_address[0:3]
        if '10.' in ip_address:
            ip_list = []
            command = 'cmd/c ipconfig | find " IPv4 Address"'
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out = cmd.communicate()

            f = open("output.txt", "w")
            f.write(str(out))
            f.close()

            with open("output.txt", 'r') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find('IPv4 Address') != -1:
                        line = line.split('  ')
                        ip_addr = line[2]
                        index1 = ip_addr.index(':')
                        index2 = len(ip_addr)
                        ip_addr = ip_addr[index1 + 1:index2 - 12]
                        print("Client IPv4 Address : " + ip_addr)
        else:
            ip_addr = IpToHex.find_ip()
            print("Client IPv4 Address : " + ip_addr)
        return ip_addr

    @staticmethod
    def ipToHex():
        list_hex_value = []
        list_hex_len = []
        ip_address = IpToHex.client_ip()
        ip_split = ip_address.split('.')
        # hex_value = hex(int(ip_split[0])) + hex(int(ip_split[1])) + hex(int(ip_split[2])) + hex(int(ip_split[3]))

        i = 0
        while i <= 3:
            hex_value = hex(int(ip_split[i])).replace('0x', '')
            list_hex_value.append(hex_value)
            hex_len = len(hex_value)
            list_hex_len.append(hex_len)
            i = i + 1

        j = 0
        while j <= 3:
            length = list_hex_len[j]
            if length != 2:
                hex_value_new = list_hex_value[j]
                hex_value_new = str(0) + hex_value_new
                list_hex_value[j] = hex_value_new
            j = j + 1

        hex_value = list_hex_value[0] + list_hex_value[1] + list_hex_value[2] + list_hex_value[3]
        return hex_value

    @staticmethod
    def Host_IPv6_address():
        Device_Type = Input_File.Device_Type
        hex_value = IpToHex.ipToHex()
        IPv6_address1 = hex_value[0:4] + ':' + hex_value[4:len(hex_value)]
        IPv6_address2 = find_prefix.IPv6_Prefix()
        if Device_Type == 'Arcadyan_IDCPE':
            IPv6_address = IPv6_address2 + '::' + IPv6_address1
            IPv6_address = IPv6_address.strip()
            print("Client IPv6 address using clat: " + str(IPv6_address))
            IpToHex.logger.info("Client IPv6 address using clat: " + str(IPv6_address))
        elif Device_Type == 'Zyxel_IDU':
            IPv6_address = IPv6_address2 + ':' + IPv6_address1
            IPv6_address = IPv6_address.strip()
            print("Client IPv6 address using clat: " + str(IPv6_address))
            IpToHex.logger.info("Client IPv6 address using clat: " + str(IPv6_address))

        return IPv6_address


