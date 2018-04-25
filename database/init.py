#!/usr/bin/python

# python script that creates a sqlite3 database
# and initilizes a table called data with 11 columns

import sqlite3

conn = sqlite3.connect('/home/pi/Documents/datalogger/database/data.db')
c = conn.cursor()

c.execute('''CREATE TABLE data (hires temp, ir, full spectrum, visible intensity, lux,temp,pressure,humidity, unknown, date, time)''')

conn.commit()
conn.close()
