# Data message format

class Firmware(BaseMessage):
    def __init__(self, src, dst, manufacturer, model, version, fw_payloads):
        # super(self, src, dst)
        # Checksum? Compress payload? fw_payloads is a dict of filenames and compressed files
        return

    def addPayload(self, payload_file):
        '''Take in the payload file and compress it'''
        #self.fw_payloads[payload_file] = zip(PathReader(payload_file))