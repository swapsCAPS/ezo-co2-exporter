#!/usr/bin/python

from prometheus_client import Gauge, start_http_server
import serial
import sys
import time
import string
from serial import SerialException

def read_line():
	"""
	taken from the ftdi library and modified to
	use the ezo line separator "\r"
	"""
	lsl = len('\r')
	line_buffer = []
	while True:
		next_char = ser.read(1)
		if next_char == '':
			break
		line_buffer.append(next_char)
		if (len(line_buffer) >= lsl and
				line_buffer[-lsl:] == list('\r')):
			break
	return ''.join(line_buffer)

def read_lines():
	"""
	also taken from ftdi lib to work with modified readline function
	"""
	lines = []
	try:
		while True:
			line = read_line()
			if not line:
				break
				ser.flush_input()
			lines.append(line)
		return lines

	except SerialException as e:
		print( "Error, ", e)
		return None

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
	ser = serial.Serial(port, 9600, timeout=0)
except serial.SerialException as e:
	print( "Could not open serial, ", e)
	sys.exit(0)

send_cmd("C,0") # turn off continuous mode
#clear all previous data
time.sleep(1)
ser.flush()

print("Polling sensor every %0.2f seconds" % delay)

start_http_server(8000)

while True:
	print('polling')
	send_cmd("R")
	lines = read_lines()
	for i in range(len(lines)):
		if lines[i][0] != '*':
			print(lines[i])
			gauge.set(lines[i])
	time.sleep(delay)
