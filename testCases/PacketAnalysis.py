import re

import pyshark

from testCases.conftest import setup
from utilities.ReadAcsTree import ReadConfig_ACS_Tree
from utilities.customLogger import LogGen
from pageObjects.Find_DUT_WanIPv6_Addr import find_Wanv6_IpAddr
from pageObjects.SSH_DUT import Ssh_To_DUT
from testCases import Input_File
from datetime import datetime


class Packet_read_ssid:
    logger = LogGen.loggen()

    @staticmethod
    def pkt_count():
        Dut_wan_ip = find_Wanv6_IpAddr.IPv6_Addr()
        acs_set_value = Ssh_To_DUT.login_ssh_ssid()
        file_name = Ssh_To_DUT.file_name
        cap = pyshark.FileCapture(file_name, display_filter="http")
        cap.load_packets()
        packet_amount = len(cap)
        print('Total HTTP packet count : ' + str(packet_amount))
        Packet_read_ssid.logger.info('Total HTTP packet count : ' + str(packet_amount))
        cap_num = []
        required_pkt_seq = []

        i = 0
        while i <= packet_amount - 1:
            cap_num.append(cap[i])
            i = i + 1

        j = 0
        while j <= packet_amount - 1:
            # with open(fname, "w", encoding="utf-8") as f:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(cap_num[j]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    ssid_tree_value = int(ReadConfig_ACS_Tree.getSSID())
                    if ssid_tree_value == 1:
                        value = 'Device.WiFi.SSID.1.SSID'
                    elif ssid_tree_value == 2:
                        value = 'Device.WiFi.SSID.2.SSID'
                    elif ssid_tree_value == 3:
                        value = 'Device.WiFi.SSID.3.SSID'
                    elif ssid_tree_value == 4:
                        value = 'Device.WiFi.SSID.4.SSID'
                    elif ssid_tree_value == 5:
                        value = 'Device.WiFi.SSID.5.SSID'
                    elif ssid_tree_value == 6:
                        value = 'Device.WiFi.SSID.6.SSID'

                    if line.find(value) != -1:
                        required_pkt_seq.append(cap_num[j])
            j = j + 1
        print('Total required ACS HTTP packets : ' + str(len(required_pkt_seq)))
        return required_pkt_seq, Dut_wan_ip, acs_set_value

    @staticmethod
    def read_required_packet():
        required_pkt_seq, DUT_WanIp, acs_set_value = Packet_read_ssid.pkt_count()
        count_seq = len(required_pkt_seq)
        post_seq_num = []
        ok_seq_num = []

        k = 0
        while k <= int(count_seq) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(required_pkt_seq[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find('Request Method: POST') != -1:
                        post_seq_num.append(str(required_pkt_seq[k]))
                    if line.find('Status Code: 200') != -1:
                        ok_seq_num.append(str(required_pkt_seq[k]))
            k = k + 1
        print('Count of post method packets : ' + str(len(post_seq_num)))
        print('Count of 200 OK method packets : ' + str(len(ok_seq_num)))
        return post_seq_num, ok_seq_num, acs_set_value

    @staticmethod
    def check_packet():
        post_seq_num, ok_seq_num, acs_set_value = Packet_read_ssid.read_required_packet()
        count_post = len(post_seq_num)
        count_ok = len(ok_seq_num)

        k = 0
        counter_post = 0
        while k <= int(count_post) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(post_seq_num[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line

                    ssid_tree_value = int(ReadConfig_ACS_Tree.getSSID())
                    if ssid_tree_value == 1:
                        ssid_value = Input_File.SSID_AP1[0]
                    elif ssid_tree_value == 2:
                        ssid_value = Input_File.SSID_AP2[0]
                    elif ssid_tree_value == 3:
                        ssid_value = Input_File.SSID_AP3[0]
                    elif ssid_tree_value == 4:
                        ssid_value = Input_File.SSID_AP4[0]
                    elif ssid_tree_value == 5:
                        ssid_value = Input_File.SSID_AP5[0]
                    elif ssid_tree_value == 6:
                        ssid_value = Input_File.SSID_AP6[0]

                    if line.find(ssid_value) != -1:
                        counter_post = counter_post + 1
            k = k + 1
            print('Post packet count with matching required : ' + str(counter_post))

            i = 0
            counter_ok = 0
            while i <= int(count_ok) - 1:
                f = open("output.txt", "w", encoding='utf-8')
                f.write(str(ok_seq_num[i]))
                f.close()

                with open("output.txt", 'r', encoding='utf-8') as fp:
                    # read all lines in a list
                    lines = fp.readlines()
                    for line in lines:
                        # check if string present on a current line
                        if line.find(ssid_value) != -1:
                            counter_ok = counter_ok + 1
                i = i + 1
            print('200 OK packet count with matching required : ' + str(counter_ok))

            if counter_ok >= 1 and counter_post >= 1:
                result = 'PASS'
            else:
                result = 'FAIL'
            return result, acs_set_value


class Packet_read_ssidPwd:
    logger = LogGen.loggen()

    @staticmethod
    def pkt_count():
        Dut_wan_ip = find_Wanv6_IpAddr.IPv6_Addr()
        acs_set_value = Ssh_To_DUT.login_ssh_ssidPwd()
        file_name = Ssh_To_DUT.file_name
        cap = pyshark.FileCapture(file_name, display_filter="http")
        cap.load_packets()
        packet_amount = len(cap)
        print('Total HTTP packet count : ' + str(packet_amount))
        Packet_read_ssidPwd.logger.info('Total HTTP packet count : ' + str(packet_amount))
        cap_num = []
        required_pkt_seq = []

        i = 0
        while i <= packet_amount - 1:
            cap_num.append(cap[i])
            i = i + 1

        j = 0
        while j <= packet_amount - 1:
            # with open(fname, "w", encoding="utf-8") as f:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(cap_num[j]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    ssid_tree_value = int(ReadConfig_ACS_Tree.getSSID())
                    if ssid_tree_value == 1:
                        value = 'Device.WiFi.SSID.1.Security.KeyPassphrase'
                    elif ssid_tree_value == 2:
                        value = 'Device.WiFi.SSID.2.Security.KeyPassphrase'
                    elif ssid_tree_value == 3:
                        value = 'Device.WiFi.SSID.3.Security.KeyPassphrase'
                    elif ssid_tree_value == 4:
                        value = 'Device.WiFi.SSID.4.Security.KeyPassphrase'
                    elif ssid_tree_value == 5:
                        value = 'Device.WiFi.SSID.5.Security.KeyPassphrase'
                    elif ssid_tree_value == 6:
                        value = 'Device.WiFi.SSID.6.Security.KeyPassphrase'

                    if line.find(value) != -1:
                        required_pkt_seq.append(cap_num[j])
            j = j + 1
        print('Total required ACS HTTP packets : ' + str(len(required_pkt_seq)))
        return required_pkt_seq, Dut_wan_ip, acs_set_value

    @staticmethod
    def read_required_packet():
        required_pkt_seq, DUT_WanIp, acs_set_value = Packet_read_ssidPwd.pkt_count()
        count_seq = len(required_pkt_seq)
        post_seq_num = []
        ok_seq_num = []

        k = 0
        while k <= int(count_seq) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(required_pkt_seq[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find('Request Method: POST') != -1:
                        post_seq_num.append(str(required_pkt_seq[k]))
                    if line.find('Status Code: 200') != -1:
                        ok_seq_num.append(str(required_pkt_seq[k]))
            k = k + 1
        print('Count of post method packets : ' + str(len(post_seq_num)))
        print('Count of 200 OK method packets : ' + str(len(ok_seq_num)))
        return post_seq_num, ok_seq_num, acs_set_value

    @staticmethod
    def check_packet():
        post_seq_num, ok_seq_num, acs_set_value = Packet_read_ssidPwd.read_required_packet()
        count_post = len(post_seq_num)
        count_ok = len(ok_seq_num)

        k = 0
        counter_post = 0
        while k <= int(count_post) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(post_seq_num[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line

                    ssid_tree_value = int(ReadConfig_ACS_Tree.getSSID())
                    if ssid_tree_value == 1:
                        ssidPwd_value = Input_File.SSID_Pwd_AP1[0]
                        acsTreevalue = 'Device.WiFi.SSID.1.Security.KeyPassphrase'
                    elif ssid_tree_value == 2:
                        ssidPwd_value = Input_File.SSID_Pwd_AP2[0]
                        acsTreevalue = 'Device.WiFi.SSID.2.Security.KeyPassphrase'
                    elif ssid_tree_value == 3:
                        ssidPwd_value = Input_File.SSID_Pwd_AP3[0]
                        acsTreevalue = 'Device.WiFi.SSID.3.Security.KeyPassphrase'
                    elif ssid_tree_value == 4:
                        ssidPwd_value = Input_File.SSID_Pwd_AP4[0]
                        acsTreevalue = 'Device.WiFi.SSID.4.Security.KeyPassphrase'
                    elif ssid_tree_value == 5:
                        ssidPwd_value = Input_File.SSID_Pwd_AP5[0]
                        acsTreevalue = 'Device.WiFi.SSID.5.Security.KeyPassphrase'
                    elif ssid_tree_value == 6:
                        ssidPwd_value = Input_File.SSID_Pwd_AP6[0]
                        acsTreevalue = 'Device.WiFi.SSID.6.Security.KeyPassphrase'

                    if line.find(acsTreevalue) != -1:
                        counter_post = counter_post + 1
            k = k + 1
            print('Post packet count with matching required : ' + str(counter_post))

            i = 0
            counter_ok = 0
            while i <= int(count_ok) - 1:
                f = open("output.txt", "w", encoding='utf-8')
                f.write(str(ok_seq_num[i]))
                f.close()

                with open("output.txt", 'r', encoding='utf-8') as fp:
                    # read all lines in a list
                    lines = fp.readlines()
                    for line in lines:
                        # check if string present on a current line
                        if line.find(ssidPwd_value) != -1:
                            counter_ok = counter_ok + 1
                i = i + 1
            print('200 OK packet count with matching required : ' + str(counter_ok))

            if counter_ok >= 1 and counter_post >= 1:
                result = 'PASS'
            else:
                result = 'FAIL'
            return result, acs_set_value


class Packet_read_ssidBroadcast:
    logger = LogGen.loggen()

    @staticmethod
    def pkt_count():
        Dut_wan_ip = find_Wanv6_IpAddr.IPv6_Addr()
        acs_set_value, broadcastValue = Ssh_To_DUT.login_ssh_ssidBroadcast()
        file_name = Ssh_To_DUT.file_name
        cap = pyshark.FileCapture(file_name, display_filter="http")
        cap.load_packets()
        packet_amount = len(cap)
        print('Total HTTP packet count : ' + str(packet_amount))
        Packet_read_ssidPwd.logger.info('Total HTTP packet count : ' + str(packet_amount))
        cap_num = []
        required_pkt_seq = []

        i = 0
        while i <= packet_amount - 1:
            cap_num.append(cap[i])
            i = i + 1

        j = 0
        while j <= packet_amount - 1:
            # with open(fname, "w", encoding="utf-8") as f:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(cap_num[j]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    ssid_tree_value = int(ReadConfig_ACS_Tree.getSSID())
                    if ssid_tree_value == 1:
                        value = 'Device.WiFi.AccessPoint.1.SSIDAdvertisementEnabled'
                    elif ssid_tree_value == 2:
                        value = 'Device.WiFi.AccessPoint.2.SSIDAdvertisementEnabled'
                    elif ssid_tree_value == 3:
                        value = 'Device.WiFi.AccessPoint.3.SSIDAdvertisementEnabled'
                    elif ssid_tree_value == 4:
                        value = 'Device.WiFi.AccessPoint.4.SSIDAdvertisementEnabled'
                    elif ssid_tree_value == 5:
                        value = 'Device.WiFi.AccessPoint.5.SSIDAdvertisementEnabled'
                    elif ssid_tree_value == 6:
                        value = 'Device.WiFi.AccessPoint.6.SSIDAdvertisementEnabled'

                    if line.find(value) != -1:
                        required_pkt_seq.append(cap_num[j])
            j = j + 1
        print('Total required ACS HTTP packets : ' + str(len(required_pkt_seq)))
        return required_pkt_seq, Dut_wan_ip, acs_set_value, broadcastValue

    @staticmethod
    def read_required_packet():
        required_pkt_seq, DUT_WanIp, acs_set_value, broadcastValue = Packet_read_ssidBroadcast.pkt_count()
        count_seq = len(required_pkt_seq)
        post_seq_num = []
        ok_seq_num = []

        k = 0
        while k <= int(count_seq) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(required_pkt_seq[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find('Request Method: POST') != -1:
                        post_seq_num.append(str(required_pkt_seq[k]))
                    if line.find('Status Code: 200') != -1:
                        ok_seq_num.append(str(required_pkt_seq[k]))
            k = k + 1
        print('Count of post method packets : ' + str(len(post_seq_num)))
        print('Count of 200 OK method packets : ' + str(len(ok_seq_num)))
        return post_seq_num, ok_seq_num, acs_set_value, broadcastValue

    @staticmethod
    def check_packet():
        post_seq_num, ok_seq_num, acs_set_value, broadcastValue = Packet_read_ssidBroadcast.read_required_packet()
        #broadcastValue =
        count_post = len(post_seq_num)
        count_ok = len(ok_seq_num)

        k = 0
        counter_post = 0
        while k <= int(count_post) - 1:
            f = open("output.txt", "w", encoding='utf-8')
            f.write(str(post_seq_num[k]))
            f.close()

            with open("output.txt", 'r', encoding='utf-8') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line

                    #if line.find(str(broadcastValue)) != -1:
                    if re.fullmatch(str(broadcastValue), line.strip()):
                        counter_post = counter_post + 1
            k = k + 1
            print('Post packet count with matching required : ' + str(counter_post))

            i = 0
            counter_ok = 0
            while i <= int(count_ok) - 1:
                f = open("output.txt", "w", encoding='utf-8')
                f.write(str(ok_seq_num[i]))
                f.close()

                with open("output.txt", 'r', encoding='utf-8') as fp:
                    # read all lines in a list
                    lines = fp.readlines()
                    for line in lines:
                        # check if string present on a current line
                        #if line.find(str(broadcastValue)) != -1:
                        if re.fullmatch(str(broadcastValue), line.strip()):
                            counter_ok = counter_ok + 1
                i = i + 1
            print('200 OK packet count with matching required : ' + str(counter_ok))

            if counter_ok >= 1 and counter_post >= 1:
                result = 'PASS'
            else:
                result = 'FAIL'
            return result, acs_set_value, broadcastValue
