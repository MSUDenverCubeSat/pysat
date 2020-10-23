import unittest
import asyncio
from pysat.Comm import Comm

class CommTests(unittest.TestCase):

    baudrate = 57600
    device = "/dev/ttyUSB0"

    def test_run_execute(self):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        loop.run_until_complete(comm.listDirectory("/home"))
