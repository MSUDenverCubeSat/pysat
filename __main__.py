from argparse import ArgumentParser
import asyncio
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
