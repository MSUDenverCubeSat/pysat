from pysat.Automatons.BaseAutomaton import BaseAutomaton
from pysat.Logger import Logger
import subprocess, serial, datetime

class SensorAutomaton (BaseAutomaton):

    def __init__(self, gps_device, gps_baudrate, local_dir):
        self.interval_sec = 5
        self.local_dir = local_dir
        self.gps_device = gps_device
        self.gps_baudrate = gps_baudrate
        self.logger = Logger("/home/pi/Temp_Files", "/home/pi/Done_Files")

    def execute(self):
        items = []

        temp = self._get_temp()
        items.append(str(temp))

        gps = self._get_gps_data()
        items.extend(gps)

        date = datetime.datetime.utcnow()
        time_stamp = date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        items.append(time_stamp)

        self._log(items)

    def _get_temp(self):
        out = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        temp = str(stdout, "UTF-8")[5:]
        return temp

    def _get_gps_data(self):
        ser = serial.Serial()
        ser.baudrate = self.gps_baudrate
        ser.port = self.gps_device
        ser.timeout = 1

        try:
            ser.open()

            if ser.isOpen():
                gpgga = ""
                gprmc = ""

                while True:
                    bytesRead = ser.readline()
                    data = str(bytesRead, "UTF-8")
                    if data[1:6] == "GPGGA":
                        gpgga = data
                    if data[1:6] == "GPRMC":
                        gprmc = data

                    if gpgga != "" and gprmc != "":
                        return [gpgga, gprmc]
            else:
                return ["No GPGGA", "No GPRMC"]
        except:
            return ["No GPGGA", "No GPRMC"]

    def _log(self, items):
        line = ""
        for item in items:
            line += "\"" + item.rstrip() + "\","
        print(line[:-1])
        self.logger.log(line[:-1])
