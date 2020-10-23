import unittest
import asyncio
from pysat.Comm import Comm

from pysat.Automatons.FtpAutomaton import FtpAutomaton

class FtpAutomatonTests(unittest.TestCase):

    baudrate = 57600
    device = "/dev/ttyUSB0"

    def test_run_execute(self,):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        a = FtpAutomaton(comm, loop, "/home/pi/files", "/home/pi/files")
        a.execute()
