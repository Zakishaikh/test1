import pyshark
from pageObjects.Ip_To_Hex_Conversion import IpToHex
from datetime import datetime
from utilities.customLogger import LogGen


class Packet_read:
    logger = LogGen.loggen()
    file_name = 'testdump_' + str(datetime.now().strftime("%d%m%Y%H%M")) + '.pcap'

    @staticmethod
    def pkt_count():
        src_ip = IpToHex.Host_IPv6_address()
        file_name = file_name = Packet_read.file_name
        cap = pyshark.FileCapture('../testCases/' + file_name, display_filter="icmpv6")
        cap.load_packets()
        packet_amount = len(cap)
        print('Ping packet count : ' + str(packet_amount))
        Packet_read.logger.info('Ping packet count : ' + str(packet_amount))
        cap_num = []
        pkt_req_seq = []
        pkt_res_seq = []

        i = 0
        while i <= packet_amount - 1:
            cap_num.append(cap[i])
            i = i + 1

        j = 0
        while j <= packet_amount - 1:
            f = open("output.txt", "w")
            f.write(str(cap_num[j]))
            f.close()
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
                if packet_format == 'request' and packet_type == 'ping':
                    pkt_req_seq.append(cap_num[j])

                elif packet_format == 'reply' and packet_type == 'ping':
                    pkt_res_seq.append(cap_num[j])
                j = j + 1
        print(str(pkt_res_seq))
        print(str(pkt_req_seq))
        return packet_amount, pkt_req_seq, pkt_res_seq, src_ip

    @staticmethod
    def read_request_packet():
        packet_amount, pkt_req_seq, pkt_res_seq, src_ip = Packet_read.pkt_count()
        count_req_seq = len(pkt_req_seq)
        req_seq_num = []

        k = 0
        counter = 0
        while k <= int(count_req_seq) - 1:
            f = open("output.txt", "w")
            f.write(str(pkt_req_seq[k]))
            f.close()
            print('Ping packet is type is : request')
            Packet_read.logger.info('Ping packet is type is : request')

            with open("output.txt", 'r') as fp:
                line = str(fp.readlines()[32:33])
                line = line.split('\\')
                line = line[1]
                line = line.split(' ')
                pcap_src_ip = line[2]
                print('Source IP in Packet capture : ' + pcap_src_ip)
                Packet_read.logger.info('Source IP in Packet capture : ' + pcap_src_ip)

            with open("output.txt", 'r') as fp:
                line = str(fp.readlines()[54:55])
                line = line.split(' ')
                line = line[1]
                line = line.split('\\')
                sequence_num = line[0]
                req_seq_num.append(sequence_num)
                print('Sequence number of ping request packet : ' + sequence_num)
                Packet_read.logger.info('Sequence number of ping request packet : ' + sequence_num)

            if pcap_src_ip == src_ip:
                counter = counter + 1
            else:
                print('Packet requirement not matched for ping request packets')
                Packet_read.logger.error('Packet requirement not matched for ping request packets')
            k = k + 1
        return counter, req_seq_num, count_req_seq

    @staticmethod
    def read_response_packet():
        packet_amount, pkt_req_seq, pkt_res_seq, dst_ip = Packet_read.pkt_count()
        count_res_seq = len(pkt_res_seq)
        res_seq_num = []

        k = 0
        counter = 0
        while k <= int(count_res_seq) - 1:
            f = open("output.txt", "w")
            f.write(str(pkt_res_seq[k]))
            f.close()
            print('Ping packet is type is : reply')
            Packet_read.logger.info('Ping packet is type is : reply')

            with open("output.txt", 'r') as fp:
                line = str(fp.readlines()[34:35])
                line = line.split('\\')
                line = line[1]
                line = line.split(' ')
                pcap_dst_ip = line[2]
                print('Destination IP in Packet capture : ' + pcap_dst_ip)
                Packet_read.logger.info('Destination IP in Packet capture : ' + pcap_dst_ip)

            with open("output.txt", 'r') as fp:
                line = str(fp.readlines()[54:55])
                line = line.split(' ')
                line = line[1]
                line = line.split('\\')
                sequence_num = line[0]
                res_seq_num.append(sequence_num)
                print('Sequence number of ping request packet : ' + sequence_num)
                Packet_read.logger.info('Sequence number of ping request packet : ' + sequence_num)

            if pcap_dst_ip == dst_ip:
                counter = counter + 1
            else:
                print('Packet requirement not matched for ping reply packets')
                Packet_read.logger.error('Packet requirement not matched for ping reply packets')
            k = k + 1
        return counter, res_seq_num, count_res_seq

    @staticmethod
    def compare_pcap():
        req_counter, req_seq_num, count_req_seq = Packet_read.read_request_packet()

        if req_seq_num[0] != req_seq_num[1] != req_seq_num[2] != req_seq_num[3]:
            req_seq_result = 'PASS'
        else:
            req_seq_result = 'FAIL'

        res_counter, res_seq_num, count_res_seq = Packet_read.read_response_packet()

        if res_seq_num[0] != res_seq_num[1] != res_seq_num[2] != res_seq_num[3]:
            res_seq_result = 'PASS'
        else:
            res_seq_result = 'FAIL'

        if req_counter == count_req_seq and res_counter == count_res_seq and req_seq_result == res_seq_result == 'PASS' and res_seq_num == req_seq_num:
            result = 'PASS'
        else:
            result = 'FAIL'
        return result
