#!/bin/bash
if pgrep mavsdk >/dev/null
then
     echo "Process is running."
else
     cd /home/pi/pysat
	 ./mavsdk_server_linux-armv7 -p 50051 --system-address serial:///dev/ttyUSB0 > /dev/null &
fi

if pgrep pysat >/dev/null
then
     echo "Process is running."
else
     cd /home/pi
	 python3 pysat --mode sat --gps_device /dev/ttyACM0 > /dev/null &
fi