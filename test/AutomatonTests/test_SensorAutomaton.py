import unittest
from pysat.Automatons.SensorAutomaton import SensorAutomaton

class SensorAutomatonTests(unittest.TestCase):

    baudrate = 9600
    gps_device = "/dev/ttyACM0"

    def test_run_execute(self,):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        a.execute()
