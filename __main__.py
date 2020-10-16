from argparse import ArgumentParser
import asyncio
import serial
from pysat.Comm import Comm
from pysat.Automatons.FtpAutomaton import FtpAutomaton


def run(args):
    loop = asyncio.get_event_loop()
    comm = Comm(loop, args.device, args.baudrate)

    a = FtpAutomaton(comm, loop, "/home/pi/files", "/home/pi/files")
    a.start()

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)

    parser.add_argument("--baudrate", type=int,
                        help="master port baud rate", default=57600)
    parser.add_argument("--device", required=True, help="serial device")
    args = parser.parse_args()

    run(args)

    '''ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/ttyACM0'

    # you must specify a timeout (in seconds) so that the
    # serial port doesn't hang
    ser.timeout = 1
    ser.open()  # open the serial port

    # print port open or closed
    if ser.isOpen():
        print('Open: ' + ser.portstr)

    for i in range(1, 10):
        bytesRead = ser.readline()  # reads in bytes followed by a newline
        print(str(bytesRead, "UTF-8"))'''
