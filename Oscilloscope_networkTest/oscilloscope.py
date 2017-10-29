#!/usr/bin/env python

import sys
import tos
from datetime import datetime, timedelta
import threading


AM_OSCILLOSCOPE = 0x93

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('version',  'int', 2),
                             ('interval', 'int', 2),
                             ('id',       'int', 2),
                             ('count',    'int', 2),
                             ('readings', 'blob', None)],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()

startcount=0
stopcount=0
init =1

before_now = datetime.now()
timebreak = before_now + timedelta(seconds=10)
print "starting time: " , before_now
while True:
	p = am.read()
	if p and p.type == AM_OSCILLOSCOPE:
	    msg = OscilloscopeMsg(p.data) 
	    if(init):
		startcount = msg.count
		init = 0
       # print msg.id, msg.count, [i<<8 | j for (i,j) in zip(msg.readings[::2], msg.readings[1::2])]
#	now = datetime.now()
#	timegap = timedelta(seconds=1)
#        timeexit = timedelta(seconds=10)
	msg.count = int(msg.count) + 1000
	print "id: ", msg.id, " count : ",  msg.count, "moteinterval : ", msg.interval, "version : ", msg.version
	print before_now
	after_now = datetime.now()
	print after_now
	if(before_now.second + 10 == after_now.second):
		stopcount = msg.count
		print "ending time:", timebreak
		print "........................... report ................................."
		print " total checking time : start ", before_now 
		print "                       stop  ", timebreak
		print " start count : ", startcount
		print " stop count  : ", stopcount 
		print " total count : ", stopcount - startcount
		print " packet per second :", (stopcount - startcount)/10 
		break;
