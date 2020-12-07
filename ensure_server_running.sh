#!/bin/bash
if pgrep python3 >/dev/null
then
     echo "Process is running."
else
     cd /home/pi
	 python3 pysat > /dev/null &
fi