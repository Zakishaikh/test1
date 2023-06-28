import pyshark
from pageObjects.Ip_To_Hex_Conversion import IpToHex
from utilities.readProperties import ReadConfig_SSH_Environment
from datetime import datetime


class Packet_read:
    file_name = 'testdump_' + str(datetime.now().strftime("%d%m%Y%H%M")) + '.pcap'

    @staticmethod
    def read_request_packet():
        try:
            file_name = Packet_read.file_name
            src_ip = IpToHex.Host_IPv6_address()
            cap = pyshark.FileCapture('../testCases/' + file_name, display_filter="icmpv6")
            cap_info_req = [cap[0], cap[2], cap[4], cap[6]]
            pkt_req_seq = []
            cap.close()

            counter = 0
            i = 0
            while i <= 3:
                f = open("output.txt", "w")
                f.write(str(cap_info_req[i]))
                f.close()

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[32:33])
                    line = line.split('\\')
                    line = line[1]
                    line = line.split(' ')
                    pcap_src_ip = line[2]
                    print('Source IP in Packet capture : ' + pcap_src_ip)

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[44:45])
                    line = line.split('\\')
                    line = line[1]
                    line = line.split(' ')
                    packet_type = str(line[2])
                    packet_type = packet_type.split('(')
                    packet_type = packet_type[1]
                    packet_type = packet_type.split(')')
                    packet_type = packet_type[0]
                    packet_format = str(line[3])
                    print('Type of packet is : ' + packet_type + ' and Format of packet is : ' + packet_format)

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[54:55])
                    line = line.split(' ')
                    line = line[1]
                    line = line.split('\\')
                    sequence_num = line[0]
                    pkt_req_seq.append(sequence_num)
                    print('Sequence number of ping request packet : ' + sequence_num)

                if pcap_src_ip == src_ip and packet_type == 'ping' and packet_format == 'request':
                    counter = counter + 1
                else:
                    print('Packet requirement not matched')
                i = i + 1
            return counter, pkt_req_seq
        except Exception as msg:
            print('Number of ping packets sent and ping packet in pcap not matched')
            counter = 0
            return counter, pkt_req_seq

    @staticmethod
    def read_response_packet():
        try:
            file_name = Packet_read.file_name
            src_ip = IpToHex.Host_IPv6_address()
            cap = pyshark.FileCapture('../testCases/' + file_name, display_filter="icmpv6")
            cap_info_res = [cap[1], cap[3], cap[5], cap[7]]
            pkt_res_seq = []
            cap.close()

            counter = 0
            j = 0
            while j <= 3:
                f = open("output.txt", "w")
                f.write(str(cap_info_res[j]))
                f.close()

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[34:35])
                    line = line.split('\\')
                    line = line[1]
                    line = line.split(' ')
                    pcap_dst_ip = line[2]
                    print('Destination IP in Packet capture : ' + pcap_dst_ip)

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[44:45])
                    line = line.split('\\')
                    line = line[1]
                    line = line.split(' ')
                    packet_type = str(line[2])
                    packet_type = packet_type.split('(')
                    packet_type = packet_type[1]
                    packet_type = packet_type.split(')')
                    packet_type = packet_type[0]
                    packet_format = str(line[3])
                    print('Type of packet is : ' + packet_type + ' and Format of packet is : ' + packet_format)

                with open("output.txt", 'r') as fp:
                    line = str(fp.readlines()[54:55])
                    line = line.split(' ')
                    line = line[1]
                    line = line.split('\\')
                    sequence_num = line[0]
                    pkt_res_seq.append(sequence_num)
                    print('Sequence number of ping request packet : ' + sequence_num)

                if pcap_dst_ip == src_ip and packet_type == 'ping' and packet_format == 'reply':
                    counter = counter + 1
                else:
                    print('Packet requirement not matched')
                j = j + 1
            return counter, pkt_res_seq
        except Exception as msg:
            print('Number of ping packets sent and ping packet in pcap not matched')
            counter = 0
            return counter, pkt_res_seq

    @staticmethod
    def compare_pcap():
        req_counter, pkt_req_seq = Packet_read.read_request_packet()
        if pkt_req_seq[0] != pkt_req_seq[1] != pkt_req_seq[2] != pkt_req_seq[3]:
            req_seq_result = 'PASS'
        else:
            req_seq_result = 'FAIL'
        res_counter, pkt_res_seq = Packet_read.read_response_packet()
        if pkt_res_seq[0] != pkt_res_seq[1] != pkt_res_seq[2] != pkt_res_seq[3]:
            res_seq_result = 'PASS'
        else:
            res_seq_result = 'FAIL'
        if req_counter == res_counter == 4 and req_seq_result == res_seq_result == 'PASS' and pkt_req_seq == pkt_res_seq:
            result = 'PASS'
        else:
            result = 'FAIL'
        return result
