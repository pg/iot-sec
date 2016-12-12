class HubUpdateHandler(object):
    def __init__(self):
        return

    def updateCheck(self):
        '''Do a check of all firmware update sites for devices known to be
        connected to the network'''
        return

    def getUpdate(self):
        '''Download, verify checksum, and store update'''
        return

    def otaUpdate(self, device):
        '''Send a firmware update over-the-air to the specified device'''
        return