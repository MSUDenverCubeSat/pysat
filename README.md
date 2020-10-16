# pysat

## Overview

pysat is is designed to run in two different modes. Satelite mode which will collect and log sensor data 
to files and the Ground station mode which will download the sensor data files from the remote machine over the connected radios. 
It's also fully compatible with Python 3.6+

Satelite Mode Features:

 - Logs GPS data

Ground Station Mode Features:

 - Downloads remote files and deletes them from the remote machine over radios

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
