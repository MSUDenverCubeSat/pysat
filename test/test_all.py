import unittest
from test.ConfigTests.test_Config import ConfigTests
from test.LoggerTests.test_UniqueFileNameEnumerator import UniqueFileNameEnumeratorTest
from test.LoggerTests.test_Logger import LoggerTests
from test.CommTests.test_Comm import CommTests
from test.AutomatonTests.test_FtpAutomaton import FtpAutomatonTests
from test.AutomatonTests.test_SensorAutomaton import SensorAutomatonTests
import subprocess
import re
import os

device = "/dev/ttyUSB0"
mavsdk_server_port = 50051

def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(ConfigTests())
    test_suite.addTest(UniqueFileNameEnumeratorTest())
    test_suite.addTest(LoggerTests())
    test_suite.addTest(CommTests())
    test_suite.addTest(FtpAutomatonTests())
    test_suite.addTest(SensorAutomatonTests())
    return test_suite


def restart_mavsdk_server(port, device):
    kill_mavsdk_server()
    start_mavsdk_server(port, device)


def start_mavsdk_server(port, device):
    server_file = os.path.join("mavsdk_server_linux-armv7")
    server_full_path = os.path.join(os.getcwd(), server_file)
    os.system(server_full_path + " -p " + str(port) + " --system-address serial://" + device + " > /dev/null &")


def kill_mavsdk_server():
    get_proc_id = subprocess.Popen(['pgrep', 'mavsdk'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

    stdout, _ = get_proc_id.communicate()
    proc_id = re.sub("[^0-9]", "", str(stdout, "UTF-8"))

    if proc_id == '':
        return

    kill_proc = subprocess.Popen(['sudo', 'kill', '-9', proc_id])
    kill_proc.communicate()


if __name__ == '__main__':
    restart_mavsdk_server(mavsdk_server_port, device)
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
