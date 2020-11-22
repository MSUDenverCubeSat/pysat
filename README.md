# Pysat

## Overview

Pysat is is designed to run in two different modes.
1. Satellite mode which will collect and log sensor data to files and the ground station.
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
   or and antenna suitably powerful, and sesnitive enough to consistently link the two primary systems
 - The team is required to fulfill an estimated orbital track to predict where the CubeSat is and point the
   the directional antenna at the CubeSat's orbital path and download the data from the CubeSat

## Install / uninstall

Install by cloning from git and making two files executable

```sh
git clone https://github.com/MSUDenverCubeSat/pysat.git
chmod 777 ensure_server_running.sh
chmod 777 mavsdk_server_linux-armv7
```

Open ensure_server_running.sh, change line 6 to your local path where you cloned the repo, change the device to match that of your radios if needed

```sh
#!/bin/bash
if pgrep mavsdk >/dev/null
then
     echo "Process is running."
else
     cd {Your local path to the repo}
	   ./mavsdk_server_linux-armv7 -p 50051 --system-address serial:///dev/ttyUSB0 > /dev/null &
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

pysat is easy to use. Simply run it using python3 and make sure to give it the device of your radio.

```sh
python3 pysat --device /dev/ttyUSB0
```
