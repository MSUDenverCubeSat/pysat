import asyncio
from pysat.Comm import Comm
from pysat.Automatons.FtpAutomaton import FtpAutomaton
from pysat.Automatons.SensorAutomaton import SensorAutomaton
from pysat.Config import Config
from pysat.Config import Mode


def run_satellite_mode(conf):
    b = SensorAutomaton(conf.gps_device, conf.gps_baudrate, conf.temp_dir, conf.final_dir)
    b.start()


def run_ground_mode(conf):
    loop = asyncio.get_event_loop()
    comm = Comm(loop, conf.comm_device, conf.comm_baudrate)
    a = FtpAutomaton(comm, loop, conf.final_dir, conf.downloaded_files_dir)
    a.start()


modes = {Mode.SAT: run_satellite_mode,
         Mode.GROUND: run_ground_mode}

if __name__ == "__main__":
    config = Config.get_config()
    modes[config.mode](config)
