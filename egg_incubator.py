#!/usr/bin/python
# -*- coding: utf-8 -*-
import linuxcnc
import sys

s = linuxcnc.stat()
c = linuxcnc.command()



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
move_axis_to(0,0,0)
move_axis_to(10,10,0)
