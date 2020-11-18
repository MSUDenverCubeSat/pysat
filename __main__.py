from argparse import ArgumentParser
import asyncio
from pysat.Comm import Comm
from pysat.Automatons.FtpAutomaton import FtpAutomaton
from pysat.Automatons.SensorAutomaton import SensorAutomaton


def run(args):

    if args.mode == "ground":
        if args.comm_device != None:
            loop = asyncio.get_event_loop()
            comm = Comm(loop, args.comm_device, args.comm_baudrate)
            a = FtpAutomaton(comm, loop, "/home/pi/Done_Files", "/home/pi/files")
            a.start()
    elif args.mode == "sat":
        b = SensorAutomaton(args.gps_device, args.gps_baudrate, "/home/pi/files")
        b.start()
    else:
        print(args.mode, "is not a valid mode")


if __name__ == "__main__":

    parser = ArgumentParser(description=__doc__)

    parser.add_argument("--comm_baudrate", type=int,
                        help="comm device baud rate", default=57600)
    parser.add_argument("--gps_baudrate", type=int,
                        help="comm device baud rate", default=9600)
    parser.add_argument("--gps_device", help="gps serial device")
    parser.add_argument("--comm_device", help="comm serial device")
    parser.add_argument("--mode", required=True, help="either sat or ground")
    args = parser.parse_args()

    run(args)
