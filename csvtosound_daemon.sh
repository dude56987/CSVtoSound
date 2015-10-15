#! /bin/bash
# run the daemon component of the software
# if ran with a currently running daemon dont relaunch
# check if csvtosound is running, if not launch it, this results in a infinte loop
if [ -f /usr/bin/csvtosound ]; then
	while ! pgrep -xc csvtosound;do
		csvtosound
	done; 
fi;

