import unittest
from unittest.mock import mock_open
from unittest.mock import patch
from pysat.Config import Config
from pysat.Config import Configuration
from dacite import exceptions


class ConfigTests(unittest.TestCase):

    def test_run_get_Config(self):
        config = Config.get_config()
        self.assertEqual(type(config), Configuration)

    def test_run_get_Config_on_bad_files(self):
        m = mock_open(read_data='''
            {
                "mode": "Bad Mode",
                "comm_device": "/dev/ttyUSB0",
                "comm_baudrate": 57600,
                "gps_device": "/dev/ttyACM0",
                "gps_baudrate": 9600,
                "sat_temp_dir": "/home/pi/Temp_Files",
                "sat_final_dir": "/home/pi/Done_Files",
                "downloaded_files_dir": "/home/pi/files"
            }''')
        with patch('builtins.open', m):
            self.assertRaises(ValueError, Config.get_config)

        m = mock_open(read_data='''
            {
                "mode": "SAT",
                "comm_device": 5,
                "comm_baudrate": 57600,
                "gps_device": "/dev/ttyACM0",
                "gps_baudrate": 9600,
                "sat_temp_dir": "/home/pi/Temp_Files",
                "sat_final_dir": "/home/pi/Done_Files",
                "downloaded_files_dir": "/home/pi/files"
            }''')
        with patch('builtins.open', m):
            self.assertRaises(exceptions.WrongTypeError, Config.get_config)

        m = mock_open(read_data='''
            {
                "mode": "SAT",
                "comm_device": "/dev/ttyUSB0",
                "comm_baudrate": "57600",
                "gps_device": "/dev/ttyACM0",
                "gps_baudrate": 9600,
                "sat_temp_dir": "/home/pi/Temp_Files",
                "sat_final_dir": "/home/pi/Done_Files",
                "downloaded_files_dir": "/home/pi/files"
            }''')
        with patch('builtins.open', m):
            self.assertRaises(exceptions.WrongTypeError, Config.get_config)
