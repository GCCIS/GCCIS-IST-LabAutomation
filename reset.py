#!/usr/bin/env python
# -*- coding: utf-8 -*-
# writen for python 2.7

# should reset a ciscos password and configuration if plugged into a 2911
# router when it is rebooting
import serial

console = serial.Serial(
        port='COM1', #windows
        #port='/dev/ttyUSB0' #what I expect it to be on Linux, dmesg when you plug in to find out
        baudrate=9600, #default baudrate
        parity='N', #default parity
        stopbits=1, #default stopbits
        bytesize=8, #default bytesize
        timeout=8
)

print(console.isOpen())

#wait until break will do something
startup_text = ''
while 'program load complete,' not in startup_text:
    startup_text += console.read(console.inWaiting())

#send break command
console.send_break()
#make sure we enter rommon and set config register
if 'rommon' in console.read(console.inWaitin()):
    console.write('confreg 0x2142\r\n')
    console.write('reset\r\n')

#watch for the initialization prompt
startup_text = ''
while '[yes/no]:' not in startup_text:
    startup_text += console.read(console.inWaiting())

#reset the device
console.write('no\r\n')
console.write('enable\r\n')
console.write('delete nvram:/startup-config\r\n')
console.write('configure terminal\r\n')
console.write('config-register 0x2102\r\n')
console.write('exit\r\n')
console.write('reboot\r\n')
console.write('no\r\n')
#console.write('...\r\n') #\r\n is windows syntax? need to write a break


