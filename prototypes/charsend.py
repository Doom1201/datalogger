#!/usr/bin/python

# send character to serial port and read
# environmental data sent back

import serial
import csv

with serial.Serial("/dev/ttyAMA0", 38400, timeout = 1) as port: 
    if port.isOpen():
        port.write(b'g')
        lines = [x.strip('\r\n') for x in port.readlines()] 
        print lines       
    else:
        print "Port not opened!"
        quit()

with open("data.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(lines)


