import asyncio
import subprocess
import re
import os
from pysat.Comm import Comm
from pysat.Automatons.FtpAutomaton import FtpAutomaton
from pysat.Automatons.SensorAutomaton import SensorAutomaton
from pysat.Config import Config
from pysat.Config import Mode


def run_satellite_mode(conf):
    b = SensorAutomaton(conf.gps_device, conf.gps_baudrate, conf.sat_temp_dir, conf.sat_final_dir)
    b.start()


def run_ground_mode(conf):
    loop = asyncio.get_event_loop()
    comm = Comm(loop, conf.mavsdk_server_address, conf.mavsdk_server_port, conf.comm_device, conf.comm_baudrate)
    a = FtpAutomaton(comm, loop, conf.sat_final_dir, conf.downloaded_files_dir)
    a.start()


def restart_mavsdk_server(port, device):
    kill_mavsdk_server()
    start_mavsdk_server(port, device)


def start_mavsdk_server(port, device):
    server_file = os.path.join("pysat", "mavsdk_server_linux-armv7")
    server_full_path = os.path.join(os.getcwd().split('pysat')[0], server_file)
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


modes = {Mode.SAT: run_satellite_mode,
         Mode.GROUND: run_ground_mode}

if __name__ == "__main__":
    config = Config.get_config()
    restart_mavsdk_server(config.mavsdk_server_port, config.comm_device)
    modes[config.mode](config)
