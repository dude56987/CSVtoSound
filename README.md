CSVtoHTML
=========

Convert CSV documents made in a spreadsheet program into HTML webpages.

##Spreadsheet Format

In the first cell of each row identify the date you want the row used on.

	The format is 1/2/1970 for January first 1970

The second cell on a row must be the time identifier. Valid identifiers are as follows...

- BREAKFAST
- LUNCH
- DINNER
- LATEMEAL

In the following cells you can add content. Content can be the following...

- Items
  - Items may be added by simply using text
- Headers
  - Use a # at the beginning of the frame, what follows will be a header
- Blank Space
  - Put a single # into the frame to add two blank lines

The amount of content that can be added is unlimited. You may also add HTML and CSS inside items.

###Example

https://raw.githubusercontent.com/dude56987/CSVtoHTML/master/example.csv

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
  - This code is intended to work with the Midori web browser on the client
  - The client hardware targeted is the Raspberry PI B+
