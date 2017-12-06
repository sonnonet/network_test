#!/usr/bin/env python

import sys
import tos
from datetime import datetime, timedelta
import threading


AM_OSCILLOSCOPE = 0xA4

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 4),
                             ('ch0Temp', 'int', 2),
                             ('ch0Humi', 'int', 2),
                             ('ch1Temp', 'int', 2),
                             ('ch1Humi', 'int', 2),
                             ],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()


while True:
	p = am.read()
	if p and p.type == AM_OSCILLOSCOPE:
	    msg = OscilloscopeMsg(p.data) 
       # print msg.id, msg.count, [i<<8 | j for (i,j) in zip(msg.readings[::2], msg.readings[1::2])]
#	now = datetime.now()
#	timegap = timedelta(seconds=1)
#        timeexit = timedelta(seconds=10)
        #humi_0 = -6 + 125 *  (msg.ch0Humi / (2^14))
        humi_0 = -2.0468 + (0.0367*msg.ch0Humi) + (-1.5955*0.000001)*msg.ch0Humi*msg.ch0Humi
        temp_0 = -(39.6) + (msg.ch0Temp * 0.01)
        humi_1 = -2.0468 + (0.0367*msg.ch1Humi) + (-1.5955*0.000001)*msg.ch1Humi*msg.ch1Humi
        temp_1 = -(39.6) + (msg.ch1Temp * 0.01)

	print "id: ", msg.srcID, " count : ",  msg.seqNo, \
          " Temp_0 : ", temp_0, "Humi_0 : ", humi_0, \
          " Temp_1 : ", temp_1, "Humi_1 : ", humi_1
