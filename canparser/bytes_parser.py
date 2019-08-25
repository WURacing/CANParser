import canparser
import re

LINE_FORMAT = '(?P<timestamp>\d+),(?P<id>[0-9A-F]+),(?P<data>[0-9A-F]{16})'
pattern = re.compile(LINE_FORMAT)

EXTENDED_MASK = 0x1FFFFFFF
STANDARD_MASK = 0x7FF


class BytesCANParser(canparser.CANParser):
    def __init__(self, dbc_file, bytes):
        super().__init__(dbc_file)
        self.bytes = bytes

    def packets(self):
        with open(self.bytes, 'rb', errors='ignore') as f:
            for line in f.readlines():
                #Sometimes the logger skips newlines
                matches = re.findall(pattern, line)
                for match in matches:
                    timestamp, msg_id, data = match

                    timestamp = int(timestamp)
                    msg_id = int(msg_id, 16) & EXTENDED_MASK
                    data = bytes.fromhex(data)

                    #Epoch and extended are assumed for now
                    packet = {
                        'timestamp': timestamp,
                        'epoch': False,
                        'extended': True,
                        'msg_id': msg_id,
                        'data': data
                    }

                    yield packet
