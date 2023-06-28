import logging
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from time import sleep
import pywintypes
import requests
import win32api
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
from utilities.customLogger import LogGen

#logger = LogGen.loggen()


class commonmethod:

    @staticmethod
    def mac_split(mac):
        x = mac.split(":")
        Mac_Add_split = x[1]
        for i in range(2, 5):
            Mac_Add_split = Mac_Add_split + ':' + x[i]
        return Mac_Add_split

    @staticmethod
    def mailAlert(toMail, filename):
        try:
            upload_URL = 'http://10.135.141.141:5000/Mail_alert_HGW_API'
            multipart_data = MultipartEncoder(
                fields={
                    # a file upload field
                    'upload': (filename, open(filename, 'rb')),

                    # plain text fields
                    'To': toMail

                }
            )

            headers = {'Content-Type': multipart_data.content_type}
            response = requests.post(upload_URL, data=multipart_data, headers=headers, timeout=30.000)
            print(response.text)
            print(response.status_code)

        except requests.exceptions.ConnectionError:
            print('This Site Can\'t be reached')

    @staticmethod
    def logger(log_message):
        date_time = datetime.now()
        print("\n[" + str(date_time) + "] " + str(log_message))
        return

    @staticmethod
    def STB_Text_Event(inputtext):
        p = subprocess.run('adb shell input text ' + inputtext, shell=True, stdin=subprocess.PIPE, capture_output=True)
        p = str(p.stdout.decode())
        if p != '':
            subprocess.run('adb shell input text ' + inputtext)
        else:
            print('Searched text ' + str(inputtext))
            sleep(1)
        return

    @staticmethod
    def STB_Key_Event(keyinput):
        key_action = {'28': 'KEYCODE_CLEAR', '3': 'ACTION_HOME', '4': 'ACTION_BACK', '19': 'ACTION_UP',
                      '20': 'ACTION_DOWN', '21': 'ACTION_LEFT', '22': 'ACTION_RIGHT', 'KEYCODE_HOME': 'ACTION_HOME',
                      'KEYCODE_BACK': 'ACTION_BACK', '23': 'ACTION_OK', '66': 'ACTION_ENTER', '24': 'ACTION_VOLUME_UP',
                      '25': 'ACTION_VOLUME_DOWN'}
        p = subprocess.run('adb shell input keyevent ' + keyinput, shell=True, stdin=subprocess.PIPE,
                           capture_output=True)
        p = str(p.stdout.decode())
        if p != '':
            subprocess.run('adb shell input keyevent ' + keyinput)
        if keyinput in key_action:
            print('KeyEvent { action=' + key_action[keyinput] + ', keyCode=' + keyinput + ' }')
        else:
            print('KeyEvent { keyCode=' + keyinput + ' }')
        sleep(1)
        return

    @staticmethod
    def get_clientSSID_list(ssid_list):
        deviceStatus = subprocess.run("adb devices ", shell=True, stdin=subprocess.PIPE,
                                      capture_output=True)
        print(deviceStatus)
        if 'offline' in str(deviceStatus.stdout):
            logging.info('------ STB OFFLINE ------')
            print('STB OFFLINE')
            sys.exit()

        print(" Device connected for adb")
        subprocess.run('adb shell am force-stop com.rjil.jiostbsetting')
        sleep(2)
        subprocess.run('adb shell am start com.rjil.jiostbsetting/.MainActivity')
        sleep(5)
        commonmethod.STB_Key_Event('19')
        commonmethod.STB_Key_Event('19')
        commonmethod.STB_Key_Event('20')
        # STB_Key_Event('20')
        commonmethod.STB_Key_Event('23')
        commonmethod.STB_Key_Event('23')
        sleep(10)
        s2 = ""
        for i in range(8):
            subprocess.run("adb shell input keyevent 20")
            sleep(2)
        # sleep(2)
        try:
            z = 0
            st = []
            n2 = []
            o2 = []
            while True:
                o2 = ",".join(n2)
                print("dump 1")
                dump = subprocess.run("adb shell uiautomator dump", shell=True, stdin=subprocess.PIPE,
                                      capture_output=True)
                print(dump)
                if 'ERROR' in str(dump.stderr):
                    print("dump 2")
                    sleep(5)
                    dump2 = subprocess.run("adb shell uiautomator dump", shell=True, stdin=subprocess.PIPE,
                                           capture_output=True)
                    print(dump2)
                    if 'ERROR' in str(dump2.stderr):
                        return n2, st

                subprocess.run("adb pull /sdcard/window_dump.xml window_dump.txt")
                s = open("window_dump.txt", 'r')
                s = str(s.read()).split("x=\"2\" text")
                e = open("window_dump.txt", 'r')
                e = str(e.read()).split("x=\"3\" text")
                for w in range(len(s)):
                    if 'com.rjil.jiostbsetting:id/tv_item_tip' in s[w]:
                        n2.append(s[w].split("resource-id")[0][2:].split('"')[0])
                        st.append('')
                for w in range(len(e)):
                    if 'com.rjil.jiostbsetting:id/tv_item_value' in e[w]:
                        st[z] = e[w].split("resource-id")[0][2:].split('"')[0]
                        z += 1

                temp = []
                for x in n2:
                    if x not in temp:
                        temp.append(x)
                    else:
                        try:
                            st.pop([i for i, n in enumerate(n2) if n == 's'][1])
                        except IndexError:
                            pass
                n2 = temp
                print(n2)
                print(st)
                if ssid_list in n2:
                    return n2, st
                if ",".join(n2) == o2:
                    return n2, st
                for i in range(9):
                    subprocess.run("adb shell input keyevent 20")
                    sleep(2)
                sleep(2)
        except IndexError:
            return "None"
        except Exception as err:
            print(err)
            pass

    @staticmethod
    def get_wifistatus(ssid, str_keypass, r):
        # print('------------ ' + str(r))
        if r > 4:
            return 'FAIL'
        status = ''
        client_ssid_list, st = commonmethod.get_clientSSID_list(ssid)
        print("Inside Common Method")
        print(client_ssid_list, st)
        sequencenumber = None
        try:
            sequencenumber = client_ssid_list.index(ssid)
            print("Sequence Number for " + str(ssid) + " is " + str(sequencenumber))
        except ValueError:
            for k in range(6):
                try:
                    sequencenumber = client_ssid_list.index(ssid)
                    print("Sequence Number for " + str(ssid) + " is " + str(sequencenumber))
                except ValueError:
                    print("Rebooting STB since SSID is not available")
                    deviceStatus = subprocess.run("adb devices ", shell=True, stdin=subprocess.PIPE,
                                                  capture_output=True)
                    print(deviceStatus)
                    print(" Device connected for adb")
                    deviceStatus = subprocess.run("adb reboot ", shell=True, stdin=subprocess.PIPE,
                                                  capture_output=True)
                    sleep(60)
                    client_ssid_list, st = commonmethod.get_clientSSID_list(ssid)
                    if ssid not in client_ssid_list:
                        # return "FAIL"
                        pass
                    else:
                        print("Inside Common Method")
                        print(client_ssid_list, st)
                        sequencenumber = client_ssid_list.index(ssid)
                        print("Sequence Number for " + str(ssid) + " is " + str(sequencenumber))
                        break
        if sequencenumber is None:
            return 'FAIL'
        # lenssid=len(client_ssid_list)-sequencenumber
        # print("Up count" + str(lenssid) + "for UP")
        for i in range(0, len(client_ssid_list) - sequencenumber - 1):
            commonmethod.STB_Key_Event('19')
            # sleep(2)
        try:
            if st[sequencenumber] == 'Connected':
                return 'Connected'
            elif st[sequencenumber] == 'Saved':
                subprocess.run("adb shell input keyevent 23 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                subprocess.run("adb shell input keyevent 20 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                subprocess.run("adb shell input keyevent 23 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                subprocess.run("adb shell input keyevent 19 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                subprocess.run("adb shell input keyevent 23 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(10)
                # print('-------------' + str(r))
                status = commonmethod.get_wifistatus(ssid, str_keypass, r)
            elif st[sequencenumber] == '':
                # if r < 3:
                r += 1
                subprocess.run("adb shell input keyevent 23 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                c = "adb shell input text " + str(str_keypass)
                subprocess.run(c, shell=True, stdin=subprocess.PIPE, capture_output=True)
                sleep(1)
                subprocess.run("adb shell input keyevent 66 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
                print('------Connecting to ' + str(ssid) + '------')
                sleep(20)
                print('------------- Attempt = ' + str(r))
                status = commonmethod.get_wifistatus(ssid, str_keypass, r)
                '''else:
                    status = 'FAIL'
                    print('-----FAIL-----' + str(r))'''
        except IndexError:
            # if r < 3:
            r += 1
            subprocess.run("adb shell input keyevent 23 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
            sleep(1)
            c = "adb shell input text " + str(str_keypass)
            subprocess.run(c, shell=True, stdin=subprocess.PIPE, capture_output=True)
            sleep(1)
            subprocess.run("adb shell input keyevent 66 ", shell=True, stdin=subprocess.PIPE, capture_output=True)
            print('------Connecting to ' + str(ssid) + '------')
            sleep(20)
            print('------------- Attempt = ' + str(r))
            status = commonmethod.get_wifistatus(ssid, str_keypass, r)
            '''else:
                status = 'FAIL'
                print('-------------error' + str(r))
                print('-----FAIL-----' + str(r))'''
        return status

    @staticmethod
    def connectWifiAndroid11(ssid, password, security, r):
        print('---------- SSID - {}, PASSWORD - {}, SECURITY - {} ----------'.format(ssid, password, security))
        str_ScanResult = ''
        commonmethod.ForgotAllNetwork()
        # print('---------------Wifi Disabled---------------')
        subprocess.run("adb shell cmd -w wifi set-wifi-enabled disabled", shell=True, stdin=subprocess.PIPE,
                       capture_output=True)
        sleep(5)
        # print('---------------Wifi Enabled---------------')
        subprocess.run("adb shell cmd -w wifi set-wifi-enabled enabled", shell=True, stdin=subprocess.PIPE,
                       capture_output=True)
        for i in range(4):
            sleep(10)
            # print('---------------Wifi Scanning Available SSID---------------')
            str_ScanResult = subprocess.run("adb shell cmd -w wifi list-scan-results", shell=True,
                                            stdin=subprocess.PIPE,
                                            capture_output=True)
            # print(str_ScanResult.stdout.decode())
            if ssid in str(str_ScanResult.stdout.decode()):
                break
        if ssid in str(str_ScanResult.stdout.decode()):
            print('---------- Connecting SSID ----------')
            # print('---------- Connecting SSID ----------')
            str_Command = 'adb shell cmd -w wifi connect-network \\"' + str(ssid) + '\\" ' + str(
                security) + ' \\"' + str(password) + '\\" '
            subprocess.run(str_Command, shell=True, stdin=subprocess.PIPE, capture_output=True)
            sleep(15)
            str_WifiStatus = subprocess.run("adb shell cmd -w wifi status", shell=True, stdin=subprocess.PIPE,
                                            capture_output=True)
            sleep(5)
            string = str_WifiStatus.stdout.decode()
            # print(string)
            pattern = '"[^"]*"'
            match = (re.search(pattern, string))
            try:
                a, b = match.span()
            except AttributeError:
                print('---------- No SSID Connected ----------')
                # print('-------------No SSID Connected-------------')
                return 'FAIL'
            str_ssidConnected = str(string[a + 1:b - 1])
            print('---------- Connected SSID - {} ----------'.format(str_ssidConnected))
            # print("SSID = " + str_ssidConnected)
            a, b = string.find("successfulTxPackets:"), string.find("successfulTxPacketsPerSecond:")
            successfulTxPackets_old = int(string[a + 21:b - 1])
            if ssid == str_ssidConnected:
                if commonmethod.pingcheck() == 'PASS':
                    status = 'PASS'
                else:
                    print('---------- Trying Ping Test Again ----------')
                    status = commonmethod.pingcheck()
                if status == 'PASS':
                    print('---------- Ping Test Passed ----------')
                    # print('---------- Ping Test Passed ----------')
                    print('---------- Playing YouTube for 60 seconds ----------')
                    # print('---------- Playing YouTube for 60 seconds ----------')
                    subprocess.run(
                        "adb shell am start -a android.intent.action.VIEW -d \"https://www.youtube.com/watch?v=VVsC2fD1BjA&ab_channel=ScenicRelaxation\"",
                        shell=True, stdin=subprocess.PIPE, capture_output=True)
                    sleep(60)
                    subprocess.run("adb shell am force-stop com.google.android.youtube", shell=True,
                                   stdin=subprocess.PIPE,
                                   capture_output=True)
                    str_WifiStatus = subprocess.run("adb shell cmd -w wifi status", shell=True, stdin=subprocess.PIPE,
                                                    capture_output=True)
                    sleep(5)
                    string = str_WifiStatus.stdout.decode()
                    # print(string)
                    a, b = string.find("successfulTxPackets:"), string.find("successfulTxPacketsPerSecond:")
                    successfulTxPackets_new = int(string[a + 21:b - 1])
                    print(
                        "---------- Before Playing YouTube successfulTxPackets = " + str(successfulTxPackets_old))
                    # print("Before Playing YouTube successfulTxPackets = " + str(successfulTxPackets_old))
                    print(
                        "---------- After Playing YouTube successfulTxPackets = " + str(successfulTxPackets_new))
                    # print("After Playing YouTube successfulTxPackets = " + str(successfulTxPackets_new))
                    if successfulTxPackets_new > successfulTxPackets_old + 500:
                        # print('---------- ' + str_ssidConnected + ' Connected ----------')
                        # print('------------' + str_ssidConnected + ' Connected------------')
                        print(
                            '---------- successfulTxPackets After Playing Youtube is greater than Before by more than 500, therefore Internet available ----------')
                        # print('successfulTxPackets After Playing YouTube is greater than Before by more than 500, therefore Internet available.')
                        return 'Connected'
                    else:
                        # print('---------- ' + str_ssidConnected + ' Connected ----------')
                        # print('------------' + str_ssidConnected + ' Connected------------')
                        print(
                            '---------- successfulTxPackets After Playing Youtube is not greater than Before by more than 500, therefore Internet not available ----------')
                        # print('successfulTxPackets After Playing YouTube is not greater than Before by more than 500, therefore Internet not available.')
                        return 'FAIL'
                else:
                    print('---------- Ping Test Failed ----------')
                    # print('------------Ping Test Failed------------')
                    return 'FAIL'
            else:
                print('---------- ' + str_ssidConnected + ' Connected in WiFi Client ----------')
                # print('---------- ' + str_ssidConnected + ' Connected ----------')
                return 'FAIL'
        else:
            print('---------- SSID Not Visible in WiFi Client ----------')
            # print('----------------WIFI SSID Not Visible----------------')
            return 'FAIL'

    @staticmethod
    def pingcheck():
        list_status = []
        print('-------- Performing Ping Test for IPv4 --------')
        command4 = ["adb", "shell", "ping", "google.com"]
        ping4 = subprocess.Popen(command4, creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        print('-------- Performing Ping Test for IPv6 --------')
        command6 = ["adb", "shell", "ping6", "google.com"]
        ping6 = subprocess.Popen(command6, creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        sleep(30)
        try:
            win32api.TerminateProcess(int(ping4._handle), -1)
        except pywintypes.error:
            print(traceback.format_exc())
            pass

        try:
            win32api.TerminateProcess(int(ping6._handle), -1)
        except pywintypes.error:
            print(traceback.format_exc())
            pass

        out4, err4 = ping4.communicate()
        print('Output = ' + out4.decode())
        print('Error for Ping4 = ' + err4.decode())
        if 'unknown host' in str(err4.decode()) or 'Network is unreachable' in str(
                err4.decode()) or 'Destination Net Unreachable' in str(err4.decode()) or 'unknown host' in str(
            out4.decode()) or 'Network is unreachable' in str(out4.decode()) or 'Destination Net Unreachable' in str(
            out4.decode()) or len(out4.decode()) == 0:
            if '64 bytes' in str(out4.decode()):
                c = str(out4.decode()).count('Destination Net Unreachable')
                n = str(err4.decode()).count('Network is unreachable')
                b = str(out4.decode()).count('64 bytes')
                print(c, n, b)
                if (c > 10 or n > 10) and b < 15:
                    list_status.append('FAIL')
                    # print('Ping Test Failed for IPv4')
                    print('-------- Ping Test Failed for IPv4 --------')
                else:
                    list_status.append('PASS')
                    # print('Ping Test Passed for IPv4')
                    print('-------- Ping Test Passed for IPv4 --------')
            else:
                list_status.append('FAIL')
                # print('Ping Test Failed for IPv4')
                print('-------- Ping Test Failed for IPv4 --------')
        else:
            list_status.append('PASS')
            # print('Ping Test Passed for IPv4')
            print('-------- Ping Test Passed for IPv4 --------')

        out6, err6 = ping6.communicate()
        print('Output = ' + out6.decode())
        print('Error for Ping6 = ' + err6.decode())
        if 'unknown host' in str(err6.decode()) or 'Network is unreachable' in str(
                err6.decode()) or 'Destination Net Unreachable' in str(err6.decode()) or 'unknown host' in str(
            out6.decode()) or 'Network is unreachable' in str(out6.decode()) or 'Destination Net Unreachable' in str(
            out6.decode()) or len(out6.decode()) == 0:
            if '64 bytes' in str(out6.decode()):
                c = str(out6.decode()).count('Destination Net Unreachable')
                n = str(err6.decode()).count('Network is unreachable')
                b = str(out6.decode()).count('64 bytes')
                print(c, n, b)
                if (c > 10 or n > 10) and b < 15:
                    list_status.append('FAIL')
                    # print('Ping Test Failed for IPv6')
                    print('-------- Ping Test Failed for IPv6 --------')
                else:
                    list_status.append('PASS')
                    # print('Ping Test Passed for IPv6')
                    print('-------- Ping Test Passed for IPv6 --------')
            else:
                list_status.append('FAIL')
                # print('Ping Test Failed for IPv6')
                print('-------- Ping Test Failed for IPv6 --------')
        else:
            list_status.append('PASS')
            # print('Ping Test Passed for IPv6')
            print('-------- Ping Test Passed for IPv6 --------')

        if 'FAIL' in list_status:
            return 'FAIL'
        else:
            return 'PASS'

    @staticmethod
    def getSSIDPassword():
        list_password = ['', '', '', '', '', '']
        infile = r"Logs/automation.log"

        with open(infile) as f:
            f = f.readlines()

        for line in f[::-1]:
            if 'SSID 1 Password' in line:
                temp = line.split(' ')
                list_password[0] = temp[8][:-1]
                break
        for line in f[::-1]:
            if 'SSID 2 Password' in line:
                temp = line.split(' ')
                # print(temp)
                list_password[1] = temp[8][:-1]
                break
        for line in f[::-1]:
            if 'SSID 3 Password' in line:
                temp = line.split(' ')
                list_password[2] = temp[8][:-1]
                break
        for line in f[::-1]:
            if 'SSID 4 Password' in line:
                temp = line.split(' ')
                list_password[3] = temp[8][:-1]
                break
        for line in f[::-1]:
            if 'SSID 5 Password' in line:
                temp = line.split(' ')
                list_password[4] = temp[8][:-1]
                break
        for line in f[::-1]:
            if 'SSID 6 Password' in line:
                temp = line.split(' ')
                list_password[5] = temp[8][:-1]
                break

        return list_password

    @staticmethod
    def getSSIDName():
        list_name = ['', '', '', '', '', '']
        infile = r"Logs/automation.log"

        with open(infile) as f:
            f = f.readlines()

        for line in f[::-1]:
            if 'SSID 1 Name' in line:
                list_name[0] = line[44:len(line) - 1]
                break
        for line in f[::-1]:
            if 'SSID 2 Name' in line:
                # print(temp)
                list_name[1] = line[44:len(line) - 1]
                break
        for line in f[::-1]:
            if 'SSID 3 Name' in line:
                list_name[2] = line[44:len(line) - 1]
                break
        for line in f[::-1]:
            if 'SSID 4 Name' in line:
                list_name[3] = line[44:len(line) - 1]
                break
        for line in f[::-1]:
            if 'SSID 5 Name' in line:
                list_name[4] = line[44:len(line) - 1]
                break
        for line in f[::-1]:
            if 'SSID 6 Name' in line:
                list_name[5] = line[44:len(line) - 1]
                break

        return list_name

    @staticmethod
    def getGHZ():
        ghz = ''
        g = open("window_dump.txt", 'r')
        g = str(g.read()).split("index=\"1\" text")
        for w in range(len(g)):
            if 'com.rjil.jiostbsetting:id/tv_item_ghz' in g[w]:
                ghz = g[w].split("resource-id")[0][2:].split('"')[0]
                break
        return ghz

    @staticmethod
    def getWifiGHZAndroid11():
        try:
            str_WifiStatus = subprocess.run("adb shell cmd -w wifi status", shell=True, stdin=subprocess.PIPE,
                                            capture_output=True)
            sleep(5)
            string = str_WifiStatus.stdout.decode()
            print(string)
            a, b = string.find("Frequency: "), string.find("MHz, Net ID:")
            int_ghz = int(string[a + 11:b])
            print(int_ghz)
            if int_ghz < 3000:
                return '2.4GHz'
            else:
                return '5GHz'
        except ValueError:
            return '--'

    @staticmethod
    def ForgotAllNetwork():
        print('--------- Wifi Enabled ----------')
        subprocess.run("adb shell cmd -w wifi set-wifi-enabled enabled", shell=True, stdin=subprocess.PIPE,
                       capture_output=True)
        sleep(3)
        print('---------- All Saved Networks Forgetting Started -----------')
        list_networkid = []
        str_WifiStatus = subprocess.run("adb shell cmd -w wifi list-networks > WifiNetworks.txt", shell=True,
                                        stdin=subprocess.PIPE,
                                        capture_output=True)
        sleep(5)
        string = str_WifiStatus.stdout.decode()
        with open('WifiNetworks.txt', 'r') as reader:
            network_list = reader.readlines()
            for testdata in network_list:
                if 'Network Id' in testdata:
                    continue
                get_network_id = testdata.split(' ')
                list_networkid.append(get_network_id[0])
        sleep(5)
        for i in list_networkid:
            command = 'adb shell cmd -w wifi forget-network' + ' ' + str(i)
            subprocess.run(command, shell=True, stdin=subprocess.PIPE, capture_output=True)
            sleep(2)

        str_WifiStatus = subprocess.run("adb shell cmd -w wifi list-networks > WifiNetworks.txt", shell=True,
                                        stdin=subprocess.PIPE,
                                        capture_output=True)
        sleep(5)
        string = str_WifiStatus.stdout.decode()
        if 'no networks' in string.lower():
            print('--------- All Saved Networks are Cleared Successfully ----------')

    @staticmethod
    def stringReplace(s):
        s = s.replace('&amp;', '&')
        s = s.replace('&lt;', '<')
        s = s.replace('&gt;', '>')
        return s

    @staticmethod
    def checkFolderStatus():
        Reports = ".//Reports//"
        Excel = ".//Excel//"
        ExcelBackup = ".//ExcelBackup//"
        ReportsBackup = ".//ReportsBackup//"
        AllReports = ".//AllReports//"

        if os.path.exists(Reports):
            shutil.rmtree(Reports)

        if os.path.exists(Excel):
            shutil.rmtree(Excel)

        if not os.path.exists(ExcelBackup):
            os.mkdir(ExcelBackup)

        if not os.path.exists(ReportsBackup):
            os.mkdir(ReportsBackup)

        if not os.path.exists(AllReports):
            os.mkdir(AllReports)

    @staticmethod
    def checkTaskTime(task, list_tasks, list_taskstime):
        i = list_tasks.index(task)
        print('---------- Latest {} message Timestamp - {}'.format(str(task), str(list_taskstime[i])))
        temp = list_taskstime[i].split(' ')[1].split(':')
        int_value = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
        return int_value

    @staticmethod
    def check_Ping4_Ping6():
        print("--------- Checking Ping 4 & 6 ---------")
        x = 20
        y = 20
        p1 = subprocess.run('ping -6 -n 20 google.com', shell=True, stdin=subprocess.PIPE, capture_output=True)
        p2 = subprocess.run('ping -4 -n 20 google.com', shell=True, stdin=subprocess.PIPE, capture_output=True)
        # print(p1.stdout.decode())
        # print(p2.stdout.decode())
        try:
            for i in p1.stdout.decode().splitlines():
                if 'Packets: Sent' in i:
                    x = int(i.split('Lost = ')[1].split(' (')[0])  # get ping 6 packet loss
                    break
        except IndexError:
            print('--------- Ping 6 Failed ---------')
            return 'FAIL'
        try:
            for i in p2.stdout.decode().splitlines():
                if 'Packets: Sent' in i:
                    y = int(i.split('Lost = ')[1].split(' (')[0])  # get ping 4 packet loss
                    break
        except IndexError:
            print('--------- Ping 4 Failed ---------')
            return 'FAIL'

        if x < 10 and y < 10:  # check packet loss
            print('--------- Ping 6 and Ping 4 Packet Loss in 20 Packets is ' + str(x) + ' and ' + str(y))
            print('--------- Ping 4 and Ping 6 Passed ---------')
            return 'PASS'  # All conditions passed
        else:  # Packet loss high
            print('--------- Ping 6 and Ping 4 Packet Loss in 20 Packets is ' + str(x) + ' and ' + str(y))
            print('--------- Ping Failed ---------')
            return 'FAIL'

    # @staticmethod
    # def client_ssid_connect(i, ssid, password, security):
    #     list_name = SSIDConfigGet.getSSIDNAME()
    #     list_pass = SSIDConfigGet.getSSIDPASSWORD()
    #     print('----------- Trying to Connect SSID {} on WiFi Client -----------'.format(str(i)))
    #     if ssid == 'Not Configured':
    #         ssid = list_name[i - 1]
    #     if password == 'Not Configured':
    #         password = list_pass[i - 1]
    #         if password == 'None':
    #             security = 'open'
    #         else:
    #             security = 'wpa2'
    #     if security == 'open':
    #         password = ''
    #         x = commonmethod.connectWifiAndroid11(ssid, password, security, r=0)
    #         if x == 'Connected':
    #             SSIDConfigSet.setSSIDNAME(i, ssid)
    #             SSIDConfigSet.setSSIDPASSWORD(i, 'None')
    #             print('----------- Accesspoint {} Connected on client -----------'.format(str(i)))
    #             return 'PASS'
    #         else:
    #             print('----------- Accesspoint {} Connection failed on client -----------'.format(str(i)))
    #             return 'FAIL'
    #     else:
    #         x = commonmethod.connectWifiAndroid11(ssid, password, security, r=0)
    #         if x == 'Connected':
    #             SSIDConfigSet.setSSIDNAME(i, ssid)
    #             SSIDConfigSet.setSSIDPASSWORD(i, password)
    #             print('----------- Accesspoint {} Connected on client -----------'.format(str(i)))
    #             return 'PASS'
    #         else:
    #             print('----------- Accesspoint {} Connection failed on client -----------'.format(str(i)))
    #             return 'FAIL'

    @staticmethod
    def pingv4_connectivity(host, count):
        command = 'cmd/c ping -4 ' + host + ' -n ' + count
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = cmd.communicate()
        output = str(out[0])
        print(output)
        error_msg_01 = output.count('unreachable')
        error_msg_02 = output.count('Request timed out')
        error_msg_03 = output.count('could not find')
        print('error unreachable count : ' + str(error_msg_01))
        print('error Request timed out count : ' + str(error_msg_02))
        print('error could not find count : ' + str(error_msg_03))
        error_count = error_msg_01 + error_msg_02 + error_msg_03
        error_count_percentage = error_count * 100 / int(count)
        error_count_percentage = int(error_count_percentage)
        print(error_count_percentage)
        if 'time=' in output and error_count_percentage <= 5:
            print('Ipv4 ping successful')
            pingv4_value = 1
        else:
            print('Ipv4 ping failed')
            pingv4_value = 0
        if pingv4_value == 1:
            result = 'PASS'
            print('Internet Connectivity over IPv4: ' + result)
        else:
            result = 'FAIL'
            print('Internet Connectivity over IPv4 : ' + result)
        return result

    @staticmethod
    def pingv6_connectivity(host, count):
        command = 'cmd/c ping -6 ' + host + ' -n ' + count
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = cmd.communicate()
        output = str(out[0])
        print(output)
        error_msg_01 = output.count('unreachable')
        error_msg_02 = output.count('Request timed out')
        error_msg_03 = output.count('could not find')
        print('error unreachable count : ' + str(error_msg_01))
        print('error Request timed out count : ' + str(error_msg_02))
        print('error could not find count : ' + str(error_msg_03))
        error_count = error_msg_01 + error_msg_02 + error_msg_03
        error_count_percentage = error_count * 100 / int(count)
        error_count_percentage = int(error_count_percentage)
        print(error_count_percentage)
        if 'time=' in output and error_count_percentage <= 5:
            print('Ipv6 ping successful')
            pingv6_value = 1
        else:
            print('Ipv6 ping failed')
            pingv6_value = 0
        if pingv6_value == 1:
            result = 'PASS'
            print('Internet Connectivity over IPv6: ' + result)
        else:
            result = 'FAIL'
            print('Internet Connectivity over IPv6: ' + result)

        return result

    @staticmethod
    def FindCurrentTime():
        from datetime import datetime
        currentDateTime = datetime.now()
        currentDate = str(currentDateTime)[0:11]
        a = str(currentDateTime).index('.')
        currentTime = str(currentDateTime)[11:a]
        h, m, s = currentTime.split(':')

        import datetime
        CurrentTime = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
        return currentDate, CurrentTime

    @staticmethod
    def TimeConversion(dt):
        import datetime
        # dt = '6/16/2023 15:55:08'
        a = dt.replace(' ', ',')
        l = a.index(',')
        acs_date = dt[0:l]
        leng = len(acs_date)
        yr = acs_date[leng - 4:leng]
        x = acs_date[0:leng - 5]
        dd = x[x.index('/') + 1:len(x)]
        if len(dd) == 1:
            dd = '0' + dd
        mm = x[0:x.index('/')]
        if len(mm) == 1:
            mm = '0' + mm
        acs_date = yr + '-' + mm + '-' + dd

        acs_time = dt[l + 1:len(dt)]
        h, m, s = acs_time.split(':')
        acs_time = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
        return acs_date, acs_time



