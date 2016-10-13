#!/usr/bin/python3

import socket
import sys
import ws2811
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 11111
RGBFILE = "/etc/luxbox/rgb.data"

print("listening at ip: ", UDP_IP, ":", UDP_PORT)

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ws2811.init()

# Loading rgb setting
try:
  f = open(RGBFILE, 'r')
  rgbdata = f.read().split(',')
  try:
    r = rgbdata[0]
  except IndexError:
    r = 0
    
  try:
    g = rgbdata[1]
  except IndexError:
    g = 0

  try:
    b = rgbdata[2]
  except IndexError:
    b = 0

  print("Loaded: ")
  print("R: " + str(r))
  print("G: " + str(g))
  print("B: " + str(b))
  f.close()
except IOError:
  print("Found no rgb.data. Expect luxbox server")

while True:
  data, addr = sock.recvfrom(4096)
  print("received message: ", data)
  jsondata = json.loads( str(data, "utf-8") );
  for area in jsondata['areas']:
    print(area)
    for value in area['values']:
      print(value)
      if value['color'] == 'r':
        r = value['value']
      elif value['color'] == 'g':
        g = value['value']
      elif value['color'] == 'b':
        b = value['value']
    ws2811.render( r, g, b)
    try:
      f = open(RGBFILE, 'w')
      f.write( str(r) + ",")
      f.write( str(g) + ",")
      f.write( str(b))
      f.close() 
    except IOError:
      print("Failed to save rgb values!")

ws2811.fini()
	
  


