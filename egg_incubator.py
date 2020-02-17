#!/usr/bin/python
# -*- coding: utf-8 -*-
import linuxcnc
import sys
import hal, time

s = linuxcnc.stat()
c = linuxcnc.command()

# create two separate hal components
#h = hal.component("passthrough")
h = hal.component("pyvcp")
#h.newpin("current_hum", hal.HAL_FLOAT, hal.HAL_IN)
#h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()

def ok_for_mdi_check():
        s.poll()
        return not s.estop and s.enabled and (s.homed.count(1) == s.axes) and (s.interp_state == linuxcnc.INTERP_IDLE)
        print ("OK")

def verify_ok_for_mdi_check():
    if not ok_for_mdi_check():
        print 'CNC machine not ready for MDI commands'
        sys.exit(1)

verify_ok_for_mdi_check()


c.mode(linuxcnc.MODE_MDI)
c.wait_complete()


#function that allows to move to specific x,y,z position

def move_axis_to(x, y, z):
    cmd = 'G0 X{0:f} Y{1:f} Z{2:f} f5'.format(x,y,z)
    print 'Command,' + cmd
    verify_ok_for_mdi_check()

    c.mdi(cmd)
    #timer to wait 60 seconds for mdi command to complete
    rv = c.wait_complete(60)
    if rv !=1:
        print 'MDI command timed out'
        sys.exit(1)

# move motor specific x,y,z position

try:
    while 1:
        time.sleep(1)
        #h['out'] = h['in']
        h['current_hum']=2.11

        #move_axis_to(0,0,0)
        #move_axis_to(3,3,0)
except KeyboardInterrupt:
    raise SystemExit
