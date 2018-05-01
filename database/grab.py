#!/usr/bin/python

# Author: Zachary Linkletter 
# ECE331 Project 2: Environmental datalogger
# Due:  5/3/18

# python script that grabs data from the serial port,
# imports the data into an sqlite3 database
# and writes JSON data to a file

import serial
import sqlite3
import datetime
import json

# open the serial port and ensure the port is open before writing character
with serial.Serial("/dev/ttyAMA0", 38400, timeout = 1) as port:
    if port.isOpen():
        port.write(b'a')
        # strip out all unnecessary characters
        lines = [x.strip('\r\n') for x in port.readlines()]

    else:
        print "Port not opened!"
        quit()

# grab datetime data from the RPi as opposed the board
# easier to use the RPi for datetime than to set the time with I2C
now = datetime.datetime.now()
# chop off the last two items in the list 'lines'
del lines[-2:]
lines += [now.strftime("%Y-%m-%d %H:%M:%S")]
# encode the list as utf8 for sqlite3 (it's picky)
[item.encode('utf8') for item in lines]

# safe way to insert data into the sql database
# prevents the destruction of the table or other security breach
# all data is taken literally from the serial port
list_string = ', '.join('?' * len(lines))
query_string = 'INSERT INTO data VALUES (%s);' % list_string

# open the database as conn
with sqlite3.connect('/home/pi/Documents/datalogger/database/database.db') as conn:
    # set row_factory as sqlite3.Row for the json encode
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    # combines the init script and grab script by only creating a table if it doesn't already exist
    c.execute('CREATE TABLE IF NOT EXISTS data (hrtemp REAL, ir INTEGER, spectrum INTEGER, visible_intensity INTEGER, lux INTEGER, temp INTEGER, pressure INTEGER, humidity INTEGER, unknown INTEGER, t TEXT)')
    # put the list lines into the database after being made safe to do so by query_string
    c.execute(query_string, lines)
    # select the last day's worth of data (24 * 60 = 1440) and fetch that data into rows
    # if there is less than 1440 rows then this query returns as much as it can, without throwing exceptions
    rows = c.execute('SELECT * FROM data LIMIT 1440 OFFSET (SELECT COUNT(*) FROM data)-1440;').fetchall()
    conn.commit()

with open('/var/www/html/data.json', 'w') as f:
    # write the returned rows as json data
    f.write(r'{"raw": ')
    f.write(json.dumps([dict(i) for i in rows]))
    f.write(r'}')

