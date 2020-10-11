from mavsdk import System
from argparse import ArgumentParser
import asyncio
from Automatons.FtpAutomaton import FtpAutomaton


async def run(args, loop):

    drone = System(mavsdk_server_address='localhost', port=50051)
    #drone = System()
    await drone.connect(system_address="serial://" + args.device + ":" + str(args.baudrate))

    a = FtpAutomaton(drone, loop, "/home/pi/files", "/home/pi/files")
    a.start()

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)

    parser.add_argument("--baudrate", type=int,
                        help="master port baud rate", default=57600)
    parser.add_argument("--device", required=True, help="serial device")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args, loop))
