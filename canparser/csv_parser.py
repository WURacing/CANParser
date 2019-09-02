import canparser
import csv
import datetime

EXTENDED_MASK = 0x1FFFFFFF
STANDARD_MASK = 0x7FF


class CSVCANParser(canparser.CANParser):
    def __init__(self, dbc_file, log_file):
        super().__init__(dbc_file)
        self.log_file = log_file

    def packets(self):
        with open(self.log_file, 'r', newline='', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = datetime.datetime(int(row["year"]), int(row["month"]),
                                         int(row["day"]), int(row["hour"]),
                                         int(row["min"]), int(row["sec"]),
                                         int(row["ms"]) * 1000)
                timestamp = int(date.timestamp() * 1000)
                msg_id = int(row["id"], 16) & EXTENDED_MASK
                data = bytes.fromhex(row["data"])

                #Epoch and extended are assumed for now
                packet = {
                    'timestamp': timestamp,
                    'epoch': False,
                    'extended': True,
                    'msg_id': msg_id,
                    'data': data
                }

                yield packet
