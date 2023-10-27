#!/usr/bin/python

from prometheus_client import Gauge, start_http_server
import serial
import sys
import time
import string
from serial import SerialException

def send_cmd(cmd):
    """
    Send command to the Atlas Sensor.
    Before sending, add Carriage Return at the end of the command.
    :param cmd:
    :return:
    """
    buf = cmd + "\r"     	# add carriage return
    try:
        ser.write(buf.encode('utf-8'))
        return True
    except SerialException as e:
        print ("Error, ", e)
        return None

port  = '/dev/ttyS0' # change to match your pi's setup
delay = 1
gauge = Gauge('ezo_co2', 'EZO CO2 Readings')

print( "Opening serial port...", port)
try:
    ser = serial.Serial(port, 9600, timeout=10000)
except serial.SerialException as e:
    print( "Could not open serial, ", e)
    sys.exit(0)

send_cmd("C,5") # turn on continuous mode
#clear all previous data
time.sleep(1)
ser.flush()

print("Polling sensor every %0.2f seconds" % delay)

start_http_server(8000)

def read_lines():
    try:
        while True:
            line = ser.read_until(b"\r", 12).decode()
            print("Received: ", line)

            try:
                co2 = int(line)
                gauge.set(co2)
            except ValueError as e:
                print("Could not parse", e)

    except SerialException as e:
        print( "Error, ", e)
        return None

read_lines()
