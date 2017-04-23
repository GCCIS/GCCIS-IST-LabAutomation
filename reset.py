#!/usr/bin/env python
# -*- coding: utf-8 -*-
# writen for python 2.7

# should reset a ciscos password and configuration if plugged into a 2911
# router when it is rebooting
# EDIT THE TWO port= LINES IF YOUR COM PORT IS DIFFERENT
import serial
import subprocess
import shlex

#baudrate = get_baudrate('COM1') # linux

console = serial.Serial(
        port='COM1', #windows
        #port='/dev/ttyUSB0', #what I expect it to be on Linux, dmesg when you plug in to find out
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
while 'rommon' not in startup_text:
    console.send_break()
    startup_text += console.read(console.inWaiting())
    print(startup_text)

#make sure we enter rommon and set config register
if 'rommon' in startup_text:
    print("entered rommon")
    console.write('confreg 0x2142\r\n')
    print("confreg 0x2142")
    console.write('reset\r\n')
    print("reset")

#TODO Should be able to change this to a one line so that port does not need to be reused
print("closing connection in case default baudrate was not used")
console.close()
console = serial.Serial(
        port='COM1', #windows
        #port='/dev/ttyUSB0', #what I expect it to be on Linux, dmesg when you plug in to find out
        baudrate=9600, #default baudrate
        parity='N', #default parity
        stopbits=1, #default stopbits
        bytesize=8, #default bytesize
        timeout=8
)
print("console opened")
print(console.isOpen())

print("entering boot read loop")
#watch for the initialization prompt
startup_text = ''
while '[yes/no]:' not in startup_text:
    startup_text += console.read(console.inWaiting())

print("Removing the current configuration")
#reset the device
console.write('no\r\n')

print("waiting for Router>")
startup_text = ''
while 'Router>' not in startup_text:
    console.write('\r\n')
    startup_text += console.read(console.inWaiting())
print(startup_text)

console.write('enable\r\n')
console.write('delete nvram:/startup-config\r\n')
console.write('\r\n')
console.write('\r\n')
console.write('write erase\r\n')
console.write('\r\n')
console.write('\r\n')
print(console.read(console.inWaiting()))
console.write('configure terminal\r\n')
console.write('config-register 0x2102\r\n')
console.write('exit\r\n')
console.write('reload\r\n')
console.write('no\r\n')
print("completed")
#console.write('...\r\n') #\r\n is windows syntax? need to write a break

def get_baudrate(device):
    command = 'stty < {0}'.format(device)
    proc_retval = subprocess.check_output(shlex.split(command))
    baudrate = int(proc_retval.split()[1])
    return baudrate
