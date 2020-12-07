from pysat.Automatons.BaseAutomaton import BaseAutomaton
from pysat.Logger import Logger
import subprocess
import serial


class SensorAutomaton (BaseAutomaton):

    def __init__(self, gps_device, gps_baudrate, temp_dir, final_dir):
        self._interval_sec = 5
        self._gps_device = gps_device
        self._gps_baudrate = gps_baudrate
        self._logger = Logger(temp_dir, final_dir)
        self._is_in_flight_mode = False

    def execute(self):
        items = []

        temp = self._get_temp()
        items.append(str(temp))

        gps = self._get_gps_data()
        items.extend(gps)

        self._log(items)

    @staticmethod
    def _get_temp():
        try:
            out = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

            stdout, stderr = out.communicate()
            temp = str(stdout, "UTF-8")[5:]
            return temp
        except:
            return "No Temp"

    def _get_gps_data(self):
        ser = serial.Serial()
        ser.baudrate = self._gps_baudrate
        ser.port = self._gps_device
        ser.timeout = 1

        try:
            ser.open()

            if ser.isOpen():

                # Put the GPS into flight mode so we can get data above 10,000 meters
                # The byte array message was gotten from the U-Blox U-Center application.
                # You can see the raw bytes it transmits for any given message sent or received
                if not self._is_in_flight_mode:
                    ser.write(b'\xB5\x62\x06\x24\x24\x00\xFF\xFF\x06\x03\x00\x00\x00\x00\x10\x27\x00\x00\x05\x00\xFA'
                              b'\x00\xFA\x00\x64\x00\x2C\x01\x00\x3C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                              b'\x52\xE8')
                    self._is_in_flight_mode = True

                gpgga = ""
                gprmc = ""

                for i in range(1, 100):
                    bytes_read = ser.readline()
                    data = str(bytes_read, "UTF-8")
                    if data[1:6] == "GPGGA":
                        gpgga = data
                    if data[1:6] == "GPRMC":
                        gprmc = data

                    if gpgga != "" and gprmc != "":
                        return [gpgga, gprmc]
                return ["No GPGGA", "No GPRMC"]
            else:
                return ["No GPGGA", "No GPRMC"]
        except:
            return ["No GPGGA", "No GPRMC"]
        finally:
            ser.close()

    def _log(self, items):
        line = ""
        for item in items:
            line += "\"" + str(item).rstrip() + "\","
        self._logger.log(line[:-1])
