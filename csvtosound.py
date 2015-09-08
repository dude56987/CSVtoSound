#! /usr/bin/python
########################################################################
# A bell system based on reading bell times from a csv file
# Copyright (C) 2015  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import urllib2,os,sys,random,datetime,time
########################################################################
def loadFile(fileName):
	try:
		#print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		#sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	#print "Finished Loading :",fileName
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return fail
	return False
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			#print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def downloadFile(fileAddress):
	try:
		print "Downloading :",fileAddress
		downloadedFileObject = urllib2.urlopen(str(fileAddress))
	except:
		print "Failed to download :",fileAddress
		return False
	lineCount = 0
	fileText = ''
	for line in downloadedFileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount+=1
	downloadedFileObject.close()
	print "Finished Loading :",fileAddress
	return fileText
########################################################################
def phaseLine(item):
	outputFileText=''
	if len(item) > 0:
		if item == '#':
			#print two blank lines
			outputFileText+=(('\t</br>'*2)+'\n')
		elif item[:12] == "#BACKGROUND=":
			# do nothing
			return ''
		elif item[0] == '#':
			# print a header
			outputFileText+=('\t<h1 class="header">'+item[1:]+'</h1>\n')
		else:
			# print a item
			outputFileText+=('\t<div class="menu_item">\n\t\t'+item+'\n\t</div>\n')
	return outputFileText
########################################################################
# Main function
########################################################################
def main():
	if '-c' in sys.argv:
		if os.path.exists('/tmp/refreshGlue'):
			# clear the file
			os.system('rm -f /tmp/refreshGlue')
			# run the script
			pass
		else:
			# exit if no refresh file is set
			exit()
	# load the config file into a string
	config = loadFile('/etc/csvtosound.cfg')
	config = config.split('\n')
	temp = []
	for item in config:
		temp.append(item.split('='))
	config = temp
	# preset variable defaults if they are not set in config file
	config_playCommand='avplay'
	config_location='/usr/share/csvtosound/csvtosound.csv'
	# set varables from config file for program
	print ("#"*80)
	print ("Reading config file...")
	print ("#"*80)
	for setting in config:
		# if the line is greater than one charcter
		if len(setting)>1:
			if setting[0][0] == '#':
				# the line is a comment, ignore it
				pass
			else:
				if setting[0] == 'playCommand':
					# CLI command to play file with
					config_playCommand=setting[1].replace(' ','').replace('\r','\n')
					print ("playCommand="+config_playCommand+';')
				elif setting[0] == 'location':
					# config file location
					config_location=setting[1].replace(' ','').replace('\r','\n')
					print ("location="+config_location+';')
				else:
					print 'Unknown config option: ',setting
	# Seprate output with lines
	# load the file into a string depending on if its online or offline
	if 'http' in config_location:
		data = downloadFile(config_location)
	else:
		data = loadFile(config_location)
	if data == False:
		print('The config file at "'+config_location+'" could not be loaded.')
		print('The program will now close.')
		exit()
	# clean line endings no matter what it is
	data = data.replace('\r\n','\n')
	data = data.replace('\r','\n')
	data = data.replace('\n\n','\n')
	tempData=''
	data=data.split('\n')
	# remove leading zeros from each line
	for item in data:
		if len(item):
			if item[0] == '0':
				tempData+=item[1:]
			else:
				tempData+=item
			tempData+='\n'
	data=tempData
	# print debug data of formated input menu
	print ("#"*80)
	print ("Printing menu data...")
	print ("#"*80)
	print data
	# year-month-day is returned so convert to month/day/year
	todayDate = datetime.date.today().isoformat().split('-')
	tempDayDate=todayDate[2]
	if tempDayDate[0] == '0':
		# remove leading zeros from day in date field
		tempDayDate=tempDayDate[1:]
	tempMonthDate=todayDate[1]
	if tempMonthDate[0] == '0':
		# remove leading zeros from month in date field
		tempMonthDate=tempMonthDate[1:]
	todayDate = tempMonthDate+'/'+tempDayDate+'/'+todayDate[0]
	########################################################
	# split up the input file and split in into an array
	data=data.split('\n')
	for line in data:
		splitline = line.split(',')
		if splitline[0] == todayDate:
			currentTime = time.localtime()
			# the fourth item in the object is hours in military time
			currentTime = int(currentTime[3])
			# hours in military time
			if (currentTime >= config_breakfastStartTime) and (currentTime < config_lunchStartTime):
			# checks if current time is between breakfast start and lunch start
				if splitline[1] == 'BREAKFAST':
					#Its BREAKFAST time
					for item in splitline[2:]:
						if item[:12] == "#BACKGROUND=":
							backgroundImage='backgrounds/extra/'
							backgroundImage+=item[12:]
						outputFileText+=phaseLine(item)
		elif splitline[0] == '#daily':
			# perform this operation every day so just check the time
			currentTime = time.localtime()
			# currentTime is in following format
			# year,month,day,hour,minute,second,weekday#,yearDay#
			# splitline is the cells
			# check the hour and compare to line 
			if int(currentTime[3])==splitline[1]:
				# compare minutes
				if int(currentTime[4])==splitline[2]:
					# check seconds
					if int(currentTime[5])==0:
						# if seconds are at 0 then play the sound
						os.system(config_playCommand+' '+splitline[3])
						# check for repeat times in command
########################################################################
main()
