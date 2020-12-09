# Pysat

## Overview

Pysat is designed to run in two different modes.
1. Satellite mode which will collect and log sensor data to files.
2. Ground Station mode which will download the sensor data files from the remote machine over the connected radios.
(The software is fully compatible with Python 3.7)

Satelite Mode Features:

 - Logs GPS data
 	- This data includes real-time location data (altitude, latitude, longitude)
 - Logs Internal temperature data
 	- Data is gathered from the internal temperature sensor of the raspberry pi
	
 - Planned Features (To be implemented based on future mission planning)
 	- X-ray spectrometer (Space Weather Mission, CubeSat Radio Interferometry Experiment (CURIE))
 		- Research particle acceleration in solar flares, performing X-ray spectroscopy of solar flares
 	- Optimal Control (Altitude and Atitude Adjustment, Satellite for Optimal Control and Imaging (SOC-I))
 		- Implement an experimental altitude and attitude for CubeSats in LEO, orbital orientation
 	- Infared Imaging (Earth Weather Mission, BeaverCube II)
 		- Ocean surface temperature, cloud composition, study climate change events for NASA earth science mission
 	- Wildfire Detection and Monitoring (Earth Weather Mission, FUEGO)
 		- Infared image monitoring and processing for early wildfire detection and monitoring 

Ground Station Mode Features:

 - Downloads remote files and deletes them from the remote machine over radios
 - It is necessary to ensure the connection between the ground station and the satellite through a tracking antenna,
   or an antenna suitably powerful, and sesnitive enough to consistently link the two primary systems
 - The team is required to fulfill an estimated orbital track to predict where the CubeSat is and point the
   the directional antenna at the CubeSat's orbital path and download the data from the CubeSat

## Install / uninstall

Install by cloning from git and making two files executable. The file mavsdk_server_linux-armv7 is specific to the arm v7 architecture. You can find the necessary file for your architecture at https://github.com/mavlink/MAVSDK/releases.

```sh
git clone https://github.com/MSUDenverCubeSat/pysat.git
chmod 777 pysat/ensure_server_running.sh
chmod 777 pysat/mavsdk_server_linux-armv7
```

Open ensure_server_running.sh, change line 6 to your local path where you cloned the repo

```sh
#!/bin/bash
if pgrep python3 >/dev/null
then
     echo "Process is running."
else
     cd {your local path}
     python3 pysat > /dev/null &
fi
```

Add the following line to your crontab making sure to substitute in your local path to the repo

```sh
*/1 * * * * sh {Your local path to the repo}/pysat/ensure_server_running.sh
```

if you have not used contab before create one by using the following command

```sh
sudo crontab -e
```
   
## Basic Usage

pysat is easy to use. Simply run it using python3.

```sh
python3 pysat
```

## Configuration
 
Under the pysat directory there is a file called config.json. This is where you should specify your device handles, baudrates, directories, and the mode (SAT or GROUND).
 
```sh
{
    "mode": "SAT",
    "comm_device": "/dev/ttyUSB0",
    "comm_baudrate": 57600,
    "gps_device": "/dev/ttyACM0",
    "gps_baudrate": 9600,
    "sat_temp_dir": "/home/pi/Temp_Files",
    "sat_final_dir": "/home/pi/Done_Files",
    "downloaded_files_dir": "/home/pi/files",
    "mavsdk_server_address": "localhost",
    "mavsdk_server_port": 50051
}
```

## Testing
 
```sh
cd {your local directory}/pysat
coverage run -m unittest
coverage report --omit=*usr*,*.local*,*test*
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
pysat/Automatons/BaseAutomaton.py        26      5    81%
pysat/Automatons/FtpAutomaton.py         54     12    78%
pysat/Automatons/SensorAutomaton.py      58      4    93%
pysat/Comm.py                            77      7    91%
pysat/Config.py                          28      0   100%
pysat/Logger.py                          37      2    95%
pysat/Result.py                           4      0   100%
pysat/UniqueFileNameEnumerator.py        32      2    94%
pysat/__init__.py                         0      0   100%
---------------------------------------------------------
TOTAL                                   316     32    90%
```

## Components Used

(CPU) Raspberry Pi 4
 - 8GB Model B
 - CPU: Quad core 64-bit ARM-Cortex A72 running at 1.5GHz
 - Power Requirements: 500mA, 5V, 3A
 - Temp Range: 0 C to 50 C, tested to -100 C
 - Wireless: 802.11 b/g/n/ac Wireless LAN
 - Bluetooth: 5.0 with BLE
 - RAM: 1, 2 and 4 Gigabyte LPDDR4
 - Display: HDMI display output up to 4Kp60
 - Ports: (x2)USB 2, (x2)USB 3, (x1)Gigabit Ethernet port, (x1)Raspberry Pi camera port
 - Software: ARMv8 Instruction Set, Currently running Python 3.7
 - GPIO Pins: (x28) user GPIO pins
 	- Up to (x6) UART
	– Up to (x6) I2C
	– Up to (x5) SPI
	– (x1) SDIO interface
	– (x1) DPI (Parallel RGB Display)
	– (x1) PCM
	– Up to (x2) PWM channels
	– Up to (x3) GPCLK outputs
 - Storage: 32GB
 
(RF Radio) RFD 900+
 - Frequency Range:  902 - 928 MHz (USA)
 - Output Power: 1W (+30dBm), controllable in 1dB steps (+/- 1dB @=20dBm typical)
 - Air Data transfer rates: 4, 8, 16, 19, 24, 32, 48, 64, 96, 128, 192 and 250 kbit/sec
 - UART data transfer rates: 2400, 4800, 9600, 19200, 38400, 57600, 115200 baud
 - Output Power: 1W (+30dBm)
 - Receive Sensitivity: >121 dBm at low data rates, high data rates
 - Dimensions: 30 mm x 57 mm x 12.8 mm (Including RF Shield, Heatsink and connector extremeties)
 - Weight: 14.5g
 - Power Supply: +5 V nominal, (+3.5 V min, +5.5 V max), ~800 mA peak at maximum power
 - Temp. Range: -40 to +85 deg C, tested operational from -73 to +123 deg C
 - Range: upwards of 40km depending on antennas and GCS setup
 - Regulations: FCC Part 15.247 (Frequency hopping and digitally modulated intentional radiators)

(Power) Afendo AFDPBES05U
 - Voltage: DC 5V/0.8A Max 
 - Weight: 150 Grams
 - Dimensions: 4.33 x 0.59 x 2.76 inches
 - Capacity: 5000 mAh 
 - Ports: USB ports (up to 2.1A/1A)
