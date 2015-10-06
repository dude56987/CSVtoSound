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
def getBlocklistPath(musicFile):
	# Pull the blocklist path out the musicFile path
	# The blocklist is stored in .blocklist in the same directory
	blocklistPath=musicFile.split(os.sep)
	blocklistPath.pop()
	blocklistPath=os.sep.join(blocklistPath)
	blocklistPath=os.path.join(blocklistPath,'.blocklist')
	if os.path.exists(blocklistPath) != True:
		os.system('touch '+blocklistPath)
	return blocklistPath
def addToBlocklist(musicFile):
	'''Add a new item to the blocklist file.'''
	blocklistPath=getBlocklistPath(musicFile)
	blocklist=loadFile(blocklistPath)
	blocklist+=musicFile+'\n'
	writeFile(blocklistPath,blocklist)
def notInBlocklist(musicFile):
	'''Check the blocklist and returns true if the file is in the
	blocklist.'''
	# load the blocklist and split on \n line endings
	blocklist=loadFile(getBlocklistPath(musicFile))
	if blocklist==False:
		print("Failed to load blocklist!")
		return False
	# if the blocklist loads split it into an array
	blocklist=blocklist.split('\n')
	if musicFile in blocklist:
		# if the file has been played
		# skip the file
		return False
	else:
		# add it to the blocklist and return false
		addToBlocklist(musicFile)
		return True
########################################################################
def runLine(splitline,config_playCommand):
	'''Reads the splitline (line split by commas into array) and plays any sound configurations included.'''
	# if seconds are at 0 then play the main sound the number of repeat times
	for i in range(int(splitline[4])):
		# check for repeat times in command
		os.system(config_playCommand+' '+os.path.join("/usr/share/csvtosound/sounds/",splitline[3]))
	if len(splitline)>=6:
		# create musicFiles array to store songs to play
		musicFiles=[]
		# if the line contains a #play or #playrandom cell create
		# a song list array
		for songPath in splitline[6:]:
			songPath=os.path.join("/usr/share/csvtosound/sounds/",songPath)
			# os.sep is operating system path seprator
			print('SONGPATH='+songPath)
			if songPath[len(songPath)-1]==os.sep:
				# if the entry ends in a slash it is a directory
				# add one song
				fileList=os.listdir(songPath)
				random.shuffle(fileList)
				escape=False
				counter=0
				#find a file that is not in the blocklist
				while escape==False:
					print('length of filelist='+str(len(fileList)))#DEBUG
					print('counter='+str(counter))#DEBUG
					# if not the blocklist or a directory
					if (('.blocklist' in fileList[counter]) != True) and ('.' in fileList[counter]):
						print('escape='+str(escape))#DEBUG
						escape=notInBlocklist(os.path.join(songPath,fileList[counter]))
						# if file is not in blocklist change filename 
						if escape==True:
							fileName=fileList[counter]	
					counter+=1
					#if all files are in the blocklist delete it
					if counter > (len(fileList)-1):
						os.system('rm '+songPath+'.blocklist')	
						# reset the counter to zero
						counter=0
				# combine the songpath and the filename
				musicFiles.append(os.path.join(songPath,fileName))
				# add all songs
				#for fileName in os.listdir(songPath):
				#	musicFiles.append(os.path.join(songPath,fileName))
			elif '.' in songPath:
				# if the entry is just a song add that song path
				musicFiles.append(songPath)
		# if music is set play it after chime
		if splitline[5]=="#play":
			#play following songs in order 
			for songFilePath in musicFiles:
				os.system(config_playCommand+' '+songFilePath)
		elif splitline[5]=="#playrandom":
			#play following songs in random order
			# shuffle the musicfile order
			random.shuffle(musicFiles)
			for songFilePath in musicFiles:
				# shuffle the music files
				# play the music files and remove them from the array
				os.system(config_playCommand+' '+musicFiles.pop())
########################################################################
def checkTime(currentTime,splitline,config_playCommand):
	'''Checks the hours and minutes compares them with splitline,
	then runs runline to perform approprate actions.'''
	# splitline is the cells
	# cells are as below
	# date,hour,minute,ring filepath,repeat times,playtype,songfile,songfile,etc.
	# check the hour and compare to line 
	if int(currentTime[3])==int(splitline[1]):
		if '--debug' in sys.argv:
			print('Hour is correct!')
		# compare minutes
		if int(currentTime[4])==int(splitline[2]):
			if '--debug' in sys.argv:
				print('Minute is correct!')
			# check seconds
			if int(currentTime[5])==0:
				runLine(splitline,config_playCommand)
########################################################################
# Main function
########################################################################
def main():
	# load the config file into a string
	config = loadFile('/etc/csvtosound.cfg')
	config = config.split('\n')
	temp = []
	for item in config:
		temp.append(item.split('='))
	config = temp
	# preset variable defaults if they are not set in config file
	config_playCommand='mplayer'
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
	while True:
		# sleep for a second to keep from hammering the processor
		time.sleep(1)
		# perform this operation every day so just check the time
		# currentTime is in following format
		# year,month,day,hour,minute,second,weekday#,yearDay#
		currentTime = time.localtime()
		# print the current time if debug mode active
		if '--debug' in sys.argv:
			print(str(currentTime[3])+':'+str(currentTime[4])+':'+str(currentTime[5]))
		# phase though the file for active lines to work on
		mute=False
		for line in data:
			splitline = line.split(',')
			if splitline[0] == todayDate:
				if splitline[1]=="#mute":
					# set mute to block playing anything
					mute=True
				# if todays date is specificly picked play sound at specified time
				else:
					if int(currentTime[3])==int(splitline[1]):
						if '--debug' in sys.argv:
							print('Hour is correct!')
						# compare minutes
						if int(currentTime[4])==int(splitline[2]):
							if '--debug' in sys.argv:
								print('Minute is correct!')
							# check seconds
							if int(currentTime[5])==0:
								if mute==False:
									runLine(splitline,config_playCommand)
			elif splitline[0] == '#daily':
				if '--debug' in sys.argv:
					print('Daily argument Reconized!')
				if mute==False:
					checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#monday':
				if int(currentTime[6])==0:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#tuesday':
				if int(currentTime[6])==1:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#wendsday':
				if int(currentTime[6])==2:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#thursday':
				if int(currentTime[6])==3:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#friday':
				if int(currentTime[6])==4:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#saturday':
				if int(currentTime[6])==5:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
			elif splitline[0] == '#sunday':
				if int(currentTime[6])==6:
					if mute==False:
						checkTime(currentTime,splitline,config_playCommand)
########################################################################
main()
