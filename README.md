CSVtoSound
=========

Use CSV document to configure a bell systems ringing times. Designed to be placed on a computer connected to a speaker system. The bell sounds are then played though the speakers configured in whatever manner the user specifies.

##Spreadsheet Format

###Example Line

 	#daily,1,0,sound.mp3,1

- First Column

In the first cell of each row identify the date you want the row used on.

	The format is 1/2/1970 for January first 1970

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

###Other Information

The amount of ring patterns that can be added is unlimited. 

###Example File

https://raw.githubusercontent.com/dude56987/CSVtoSound/master/example.csv

##Setup Information

- Download the source 
  - On github you can download a zipfile on the right side of the webpage.
  - You must extract the source if it is in a zipfile
- Open a terminal in the directory of the source
- Type "make full-install"
  - That will install the program and its necessary components
  - This will install and setup apache if its not installed already
 
###Additional Setup Information

- Server Info
  - This code is intended to run on Ubuntu Server Edition
- Client Info
  - The client hardware targeted is the Raspberry PI B+
