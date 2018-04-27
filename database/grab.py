#!/usr/bin/python

# python script that grabs data from the serial port,
# imports the data into an sqlite3 database
# and writes JSON data to a file

import serial
import sqlite3
import datetime
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

with serial.Serial("/dev/ttyAMA0", 38400, timeout = 1) as port:
    if port.isOpen():
        port.write(b'a')
        lines = [x.strip('\r\n') for x in port.readlines()]

    else:
        print "Port not opened!"
        quit()

now =datetime.datetime.now()
del lines[-2:]
dt = now.strftime("%Y/%m/%d %H:%M:%S")
lines += [dt[0:10],dt[11:]]
[item.encode('utf8') for item in lines]

list_string = ', '.join('?' * len(lines))
query_string = 'INSERT INTO data VALUES (%s);' % list_string

with sqlite3.connect('/home/pi/Documents/datalogger/database/database.db') as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (hires REAL, ir INTEGER, spectrum INTEGER, visible_intensity INTEGER, lux INTEGER, temp INTEGER, pressure INTEGER, humidity INTEGER, unknown INTEGER, _date TEXT, _time TEXT)')
    c.execute(query_string, lines)
    rows = c.execute('SELECT * FROM data LIMIT 1440 OFFSET (SELECT COUNT(*) FROM data)-1440;').fetchall()
    conn.commit()

with open('/var/www/html/data', 'w') as f:
    f.write(json.dumps([dict(i) for i in rows], sort_keys=True))

