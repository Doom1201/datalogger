#!/usr/bin/python

# python script that grabs data from the serial port
# and imports the data into an sqlite3 database

import serial
import sqlite3

with serial.Serial("/dev/ttyAMA0", 38400, timeout = 1) as port:
    if port.isOpen():
        port.write(b'a')
        lines = [x.strip('\r\n') for x in port.readlines()]

    else:
        print "Port not opened!"
        quit()

list_string = ', '.join('?' * len(lines))
query_string = 'INSERT INTO data VALUES (%s);' % list_string

conn = sqlite3.connect('/home/pi/Documents/datalogger/database/data.db')
c = conn.cursor()

c.execute(query_string, lines)

c.execute('SELECT * FROM data')
print c.fetchall()

conn.commit()
conn.close()
