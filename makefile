help:
	#####################################################
	# Type "make install" to install the program        #
	# Type "make uninstall" to remove the program       #
	#####################################################
	# The below commands are for developers             #
	#####################################################
	# -Type "sudo make test" to install and run the     #
	#   program                                         #
	# -Type "sudo make test-install" to install without #
	#   setting up cron                                 #
	#####################################################
debug:
	csvtosound --debug
full-install:
	# install mplayer to play files
	apt-get install mplayer --assume-yes
	# setup csvtosound and run it
	make install
install:
	# create directories
	sudo mkdir -p /etc/csvtosound
	sudo mkdir -p /usr/share/csvtosound
	sudo mkdir -p /usr/share/csvtosound/sounds
	# copy over the sounds to the sound folder
	sudo cp -rv sounds/. /usr/share/csvtosound/sounds/
	# copy over the program
	sudo cp -fv csvtosound.py /usr/bin/csvtosound
	# copy over the config file to /etc
	sudo cp -fv csvtosound.cfg /etc/csvtosound.cfg
	# copy over daemon script
	sudo cp -fv csvtosound_daemon.sh /usr/bin/csvtosound_daemon
	# make it executable by root only
	sudo chmod ugo-xwr /usr/bin/csvtosound_daemon
	sudo chmod u+xr /usr/bin/csvtosound_daemon
	# add the schedule if it dont exist
	#sudo touch /usr/share/csvtosound/csvtosound.csv
	sudo cp example.csv /usr/share/csvtosound/csvtosound.csv
	# link the file to be in /usr/bin/ and make it executable by root only
	sudo chmod ugo-xwr /usr/bin/csvtosound
	sudo chmod u+xr /usr/bin/csvtosound
	# create user bellsystem user if they dont exist
	useradd --home /usr/share/csvtosound/ bellsystem || echo "User Exists!"
	# set csvtosound config directory ownership to bellsystem
	# this is for a user to login to remotely manage the sound system
	chown -R bellsystem /usr/share/csvtosound/ 
	# copy over the cron jobs
	sudo cp -fv cron /etc/cron.d/csvtosound
project-report:
	sudo apt-get install gitstats gource --assume-yes
	rm -vr report/ || echo "No existing report..."
	mkdir -p report
	mkdir -p report/webstats
	# write the index page
	echo "<html style='margin:auto;width:800px;text-align:center;'><body>" > report/index.html
	echo "<a href='webstats/index.html'><h1>WebStats</h1></a>" >> report/index.html
	echo "<a href='log.html'><h1>Log</h1></a>" >> report/index.html
	echo "<video src='video.mp4' width='800' controls>" >> report/index.html
	echo "<a href='video.mp4'><h1>Gource Video Rendering</h1></a>" >> report/index.html
	echo "</video>" >> report/index.html
	echo "</body></html>" >> report/index.html
	# write the log to a webpage
	echo "<html><body>" > report/log.html
	echo "<h1><a href='index.html'>Back</a></h1>" >> report/log.html
	# generate the log into a variable
	git log --stat > report/logInfo
	echo "<code><pre>" >> report/log.html
	cat report/logInfo >> report/log.html
	echo "</pre></code>" >> report/log.html
	rm report/logInfo
	echo "</body></html>" >> report/log.html
	# generate git statistics
	gitstats -c processes='8' . report/webstats
	# generate a video with gource
	gource --max-files 0 -s 1 -c 4 -1280x720 -o - | avconv -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 8 -bf 0 report/video.mp4
