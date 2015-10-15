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
install-debian: install
	# install openssh-server
	sudo apt-get install openssh-server
	# install and enable ufw
	sudo apt-get install ufw --assume-yes
	# allow ssh in the firewall
	sudo ufw allow port 22
	# install mplayer to play files
	sudo apt-get install mplayer --assume-yes
	# set the timezone
	sudo dpkg --reconfigure tzdata
	# create user to launch program under
	sudo adduser bellsystem
	# modify users group permissions to add them to audio
	sudo usermod -a -G audio bellsystem
	# add the program to /home/bellsystem/.profile 

	# add autologin user to /etc/inittab on tty2

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
test-install:
	# dont make the cron job work
	# create directories -p is like force
	sudo mkdir -p /usr/share/signage
	sudo mkdir -p /usr/share/signage/default
	sudo mkdir -p /var/www/html/CSVtoSound
	# copy over the program
	sudo cp -fv CSVtoSound.py /usr/bin/CSVtoSound
	# copy over the default css
	sudo cp -fv style.css /usr/share/signage/style.css
	# copy over the default users for admin area
	sudo cp -fv users.cfg /usr/share/signage/users.cfg
	# copy over the config file to /etc
	sudo cp -fv CSVtoSound.cfg /etc/CSVtoSound.cfg
	# link the file to be in /usr/bin/ and make it executable
	sudo chmod +x /usr/bin/CSVtoSound
	# copy over the cron jobs
	sudo cp -fv cron /etc/cron.d/csvtosound
uninstall:
	# nuke out the files pushed in install
	# echo everything in case user has changed locations
	sudo rm -rvf /var/www/html/CSVtoSound/ || echo 'lol'
	sudo rm /etc/cron.hourly/CSVtoSound || echo 'lol'
	sudo rm /usr/bin/CSVtoSound || echo 'lol'
	sudo rm /etc/CSVtoSound.cfg || echo 'lol'
	sudo rm -rvf /usr/share/signage/ || echo 'lol'
	# clean up cron entries
	sudo sed -i "s/\*\/3\ \*\ \*\ \*\ \*\ root\ CSVtoSound\ \-c//g" /etc/crontab
	sudo bash -c "cat /etc/crontab | tr -s '\n' > /etc/crontab"
push:
	# nuke the zipfile if it already exists
	rm CSVtoSound.zip || echo 'already gone yo!'
	# zip up the program into CSVtoSound.zip
	zip -rv CSVtoSound.zip CSVtoSound.cfg CSVtoSound.py makefile style.css backgrounds
	# create directory for CSVtoSound if it does not yet exist
	sudo mkdir -p /var/www/html/CSVtoSound
	# copy the zipfile into the web directory
	sudo cp -v CSVtoSound.zip /var/www/html/CSVtoSound
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
