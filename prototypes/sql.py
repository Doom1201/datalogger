#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('/home/pi/Documents/datalogger/database/testing.db')
c = conn.cursor()

c.execute('''CREATE TABLE data
        (date, time, hires temp, ir, full spectrum, visible intensity, lux, temp, pressure,
        humidity)''')
c.execute("INSERT INTO data VALUES ('2/2/2000','10:00:00','29.937500','7082','22650','15569','582','3031','9997816','22223')")

t = ('10:00:00',)

c.execute('SELECT * FROM data WHERE time=?', t)
print c.fetchone()

conn.commit()
conn.close()
