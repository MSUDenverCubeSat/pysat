#!/bin/bash
if pgrep mavsdk >/dev/null
then
     echo "Process is running."
else
     cd /home/pi/pysat
	 ./mavsdk_server_linux-armv7 -p 50051 --system-address serial:///dev/ttyUSB0 > /dev/null &
fi