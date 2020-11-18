import unittest
import shutil
import os
import time
from pysat.Automatons.SensorAutomaton import SensorAutomaton


class SensorAutomatonTests(unittest.TestCase):

    baudrate = 9600
    gps_device = "/dev/ttyACM0"
    temp_dir = "/home/pi/Temp_Files"
    final_dir = "/home/pi/Done_Files"

    def setUp(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

        try:
            shutil.rmtree(self.final_dir)
        except:
            pass

    def test_run_execute_twice(self):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        self.assertEqual(a.__active__, False)
        a.start()
        self.assertEqual(a.__active__, True)

        time.sleep(a.interval_sec * 2 + 2)
        self.assertEqual(a.__active__, True)
        a.stop()
        self.assertEqual(a.__active__, False)

        time.sleep(a.interval_sec)
        self.assertEqual(a.__active__, False)

        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), True)

        file1 = open(os.path.join(self.temp_dir, "file1.txt"), "r")
        lines = file1.readlines()
        file1.close()
        self.assertEqual(lines.__len__(), 2)
        for line in lines:
            parts = line.split("\",\"")
            self.assertEqual(parts.__len__(), 3)

        self.setUp()

    def test_run_start_stop(self):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        self.assertEqual(a.__active__, False)
        a.start()
        self.assertEqual(a.__active__, True)

        time.sleep(a.interval_sec + 1)
        self.assertEqual(a.__active__, True)
        a.stop()
        self.assertEqual(a.__active__, False)

        time.sleep(a.interval_sec)
        self.assertEqual(a.__active__, False)

        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), True)

        file1 = open(os.path.join(self.temp_dir, "file1.txt"), "r")
        lines = file1.readlines()
        file1.close()
        self.assertEqual(lines.__len__(), 1)
        parts = lines[0].split("\",\"")
        self.assertEqual(parts.__len__(), 3)

        self.setUp()

    def test_run_execute(self):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        a.execute()

        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), True)

        file1 = open(os.path.join(self.temp_dir, "file1.txt"), "r")
        lines = file1.readlines()
        file1.close()
        self.assertEqual(lines.__len__(), 1)
        parts = lines[0].split("\",\"")
        self.assertEqual(parts.__len__(), 3)

        self.setUp()

    def test_run_get_temp(self):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        temp = a._get_temp()

        self.assertEqual(temp.__contains__("No"), False)

        self.setUp()

    def test_run_get_gps_data(self):

        a = SensorAutomaton(self.gps_device, self.baudrate, "/home/pi/files")
        gps_data = a._get_gps_data()
        for i in range(0, 10):
            gps_data.extend(a._get_gps_data())

        got_good_data = False
        for datum in gps_data:
            if datum.__contains__("No") is False:
                got_good_data = True
                break
        self.assertEqual(got_good_data, True)

        self.setUp()
