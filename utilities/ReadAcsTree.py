import configparser

config = configparser.RawConfigParser()  # To read data from config.ini


# config = configparser.ConfigParser()


class ReadConfig_ACS_Tree:
    config.read('../Configurations/AcsTreeConfig.ini')

    @staticmethod
    def getSSID1():
        ssid1 = str(config.get('ACS Tree info', 'SSID1'))
        return ssid1

    @staticmethod
    def getSSID2():
        ssid2 = str(config.get('ACS Tree info', 'SSID2'))
        return ssid2

    @staticmethod
    def getSSID3():
        ssid3 = str(config.get('ACS Tree info', 'SSID3'))
        return ssid3

    @staticmethod
    def getSSID4():
        ssid4 = str(config.get('ACS Tree info', 'SSID4'))
        return ssid4

    @staticmethod
    def getSSID5():
        ssid5 = str(config.get('ACS Tree info', 'SSID5'))
        return ssid5

    @staticmethod
    def getSSID6():
        ssid6 = str(config.get('ACS Tree info', 'SSID6'))
        return ssid6

    @staticmethod
    def getSSID():
        ssid = str(config.get('ACS Tree info', 'ssid'))
        return ssid

    @staticmethod
    def setSSID(value):
        path = '../Configurations/AcsTreeConfig.ini'
        config.set('ACS Tree info', 'ssid', value)

        with open(path, 'w') as config_file:
            config.write(config_file)

    @staticmethod
    def getSSIDPwd1():
        ssidPwd1 = str(config.get('ACS Tree info', 'ssidPwd1'))
        return ssidPwd1

    @staticmethod
    def getSSIDPwd2():
        ssidPwd2 = str(config.get('ACS Tree info', 'ssidPwd2'))
        return ssidPwd2

    @staticmethod
    def getSSIDPwd3():
        ssidPwd3 = str(config.get('ACS Tree info', 'ssidPwd3'))
        return ssidPwd3

    @staticmethod
    def getSSIDPwd4():
        ssidPwd4 = str(config.get('ACS Tree info', 'ssidPwd4'))
        return ssidPwd4

    @staticmethod
    def getSSIDPwd5():
        ssidPwd5 = str(config.get('ACS Tree info', 'ssidPwd5'))
        return ssidPwd5

    @staticmethod
    def getSSIDPwd6():
        ssidPwd6 = str(config.get('ACS Tree info', 'ssidPwd6'))
        return ssidPwd6

    @staticmethod
    def getAp1():
        ap = str(config.get('ACS Tree info', 'ap1'))
        return ap

    @staticmethod
    def getAp2():
        ap = str(config.get('ACS Tree info', 'ap2'))
        return ap

    @staticmethod
    def getAp3():
        ap = str(config.get('ACS Tree info', 'ap3'))
        return ap

    @staticmethod
    def getAp4():
        ap = str(config.get('ACS Tree info', 'ap4'))
        return ap

    @staticmethod
    def getAp5():
        ap = str(config.get('ACS Tree info', 'ap5'))
        return ap

    @staticmethod
    def getAp6():
        ap = str(config.get('ACS Tree info', 'ap6'))
        return ap

    @staticmethod
    def getInterface1Stats():
        InterfaceNum = str(config.get('ACS Tree info', 'interface1Stat'))
        return InterfaceNum

    @staticmethod
    def getInterface2Stats():
        InterfaceNum = str(config.get('ACS Tree info', 'interface2Stat'))
        return InterfaceNum

    @staticmethod
    def getInterface3Stats():
        InterfaceNum = str(config.get('ACS Tree info', 'interface3Stat'))
        return InterfaceNum

    @staticmethod
    def getInterface4Stats():
        InterfaceNum = str(config.get('ACS Tree info', 'interface4Stat'))
        return InterfaceNum

