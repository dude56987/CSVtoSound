CSVtoSound
=========

Use CSV document to configure a bell systems ringing times. Designed to be placed on a computer connected to a speaker system. The bell sounds are then played though the speakers configured in whatever manner the user specifies.

##Spreadsheet Format

###Example Line

 	#daily,1,0,sound.mp3,1

###First Column

In the first cell of each row identify the date you want the row used on.

	The format is 1/1/1970 for January first 1970.

Dates can also contain regular expressions.

	For example 1/*/* would run any day in January of any year.

Repeating dates are repsented as hashtags.

- \#daily
  - Will play the patern every day at the specified time.
- \#monday
  - Will play the patern every monday at the specified time. 
- \#tuesday
  - Will play the pattern every tuesday at the specified time. 
- \#wendsday
  - Will play the pattern every wendsday at the specified time. 
- \#thursday
  - Will play the pattern every thursday at the specified time.
- \#friday
  - Will play the pattern every friday at the specified time. 
- \#saturday
  - Will play the pattern every saturday at the specified time. 
- \#sunday
  - Will play the pattern every sunday at the specified time. 

###Second Column
- The second column is the hour of the day you want the sound to play. 
- The time is in military time.

###Third Column
- The third column is the minute of the hour you want to play the sound on.

###Fourth Column
- The fourth column is the filepath to the soundfile to be used.

###Fifth Column
- The number of times to repeat the tone

###Sixth Column
- Optional
- Flag to play songs after bell tones
- Can be either \#play or \#playrandom
  - \#play will play each entry in the order specified
  - \#playrandom will play one of the song entries randomly

###Seventh+ Columns
- All additional column entries on a line are for songs to be played by as specified in the sixth column.
- Entries in these columns must be either a file path or a directory path.
  - File paths must be specific and located on the server system.
  - Directory paths must be located on the same system.
	- One file out of the folder will be used.
	- Files used are added to the blocklist so files will not repeat till all files in directory have been exhausted.

###Special Cases
- You can mute all sounds for the entire day by placing #mute into the second column on a specific date.
  - If you do want to mute a day you should place the mute entry at the top of the document so it receives priority.
  - Below is a example of a mute entry.

    1/1/1970,#mute
    
###Other Information

The amount of ring patterns that can be added is unlimited. 

###Example File

https://raw.githubusercontent.com/dude56987/CSVtoSound/master/example.csv

##Setup Information

###Manual Install

- Download the source 
  - On github you can download a zipfile on the right side of the webpage.
  - You must extract the source if it is in a zipfile
- Open a terminal in the directory of the source
- Type "make full-install"
  - That will install the program and its necessary components
  - This will install and setup apache if its not installed already
 
###CLI Oneline Install

	pkexec bash -c "apt-get install git make gdebi --assume-yes && git clone https://github.com/dude56987/csvtosound -o /tmp/csvtosound && cd /tmp/csvtosound && make install && rm -rvf /tmp/csvtosound"

###Additional Setup Information

- Server Info
  - This code is intended to run on Ubuntu Server Edition
