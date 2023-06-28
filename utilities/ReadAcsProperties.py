import configparser

config = configparser.RawConfigParser()  # To read data from config.ini


# config = configparser.ConfigParser()


class ReadConfig_ACS_Environment:
    config.read('../Configurations/ACSConfig.ini')

    @staticmethod
    def getACSUrL():
        url = str(config.get('ACS info', 'baseURL'))
        return url

    @staticmethod
    def getUsername():
        username = str(config.get('ACS info', 'username'))
        return username

    @staticmethod
    def getPassword():
        password = str(config.get('ACS info', 'password'))
        return password

    @staticmethod
    def getDeviceSerial():
        device_serial = str(config.get('ACS info', 'device_serial'))
        return device_serial
