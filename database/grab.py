#!/usr/bin/python

# python script that grabs data from the serial port,
# imports the data into an sqlite3 database
# and writes JSON data to a file

import serial
import sqlite3
import datetime
import json

with serial.Serial("/dev/ttyAMA0", 38400, timeout = 1) as port:
    if port.isOpen():
        port.write(b'a')
        lines = [x.strip('\r\n') for x in port.readlines()]

    else:
        print "Port not opened!"
        quit()

now =datetime.datetime.now()
del lines[-2:]
lines += [now.strftime("%Y-%m-%d %H:%M:%S")]
[item.encode('utf8') for item in lines]

list_string = ', '.join('?' * len(lines))
query_string = 'INSERT INTO data VALUES (%s);' % list_string

with sqlite3.connect('/home/pi/Documents/datalogger/database/database.db') as conn:
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (hrtemp REAL, ir INTEGER, spectrum INTEGER, visible_intensity INTEGER, lux INTEGER, temp INTEGER, pressure INTEGER, humidity INTEGER, unknown INTEGER, t TEXT)')
    c.execute(query_string, lines)
    rows = c.execute('SELECT * FROM data LIMIT 1440 OFFSET (SELECT COUNT(*) FROM data)-1440;').fetchall()
    conn.commit()

with open('/var/www/html/data', 'w') as f:
    f.write(r'{"raw": ')
    f.write(json.dumps([dict(i) for i in rows]))
    f.write(r'}')

