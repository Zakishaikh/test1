import configparser

config = configparser.RawConfigParser()  # To read data from config.ini


# config = configparser.ConfigParser()


class ReadConfig_GUI_Environment:
    config.read('../Configurations/GUIconfig.ini')

    @staticmethod
    def getGatewayUrL():
        url = str(config.get('GUI info', 'baseURL'))
        return url

    @staticmethod
    def getUsername():
        username = str(config.get('GUI info', 'username'))
        return username

    @staticmethod
    def getPassword():
        password = str(config.get('GUI info', 'password'))
        return password

    @staticmethod
    def getDefaultPassword():
        password = str(config.get('GUI info', 'defaultPassword'))
        return password


class ReadConfig_SSH_Environment_Arc_IDCPE:
    config.read('../Configurations/SSHconfig.ini')

    @staticmethod
    def getGatewayIp():
        GatewayIp = str(config.get('SSH Info Arc IDCPE', 'GatewayIp'))
        return GatewayIp

    @staticmethod
    def getSSHUsename():
        username = str(config.get('SSH Info Arc IDCPE', 'SSH_username'))
        return username

    @staticmethod
    def getSSHPassword():
        password = str(config.get('SSH Info Arc IDCPE', 'SSH_password'))
        return password


class ReadConfig_SSH_Environment_Zyxel_IDU:
    config.read('../Configurations/SSHconfig.ini')

    @staticmethod
    def getGatewayIp():
        GatewayIp = str(config.get('SSH Info Zyxel IDU', 'GatewayIp'))
        return GatewayIp

    @staticmethod
    def getSSHUsename():
        username = str(config.get('SSH Info Zyxel IDU', 'SSH_username'))
        return username

    @staticmethod
    def getSSHPassword():
        password = str(config.get('SSH Info Zyxel IDU', 'SSH_password'))
        return password
