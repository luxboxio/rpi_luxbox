#!/usr/bin/python3

import socket
import sys
import ws2811
import json
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 11111
RGBFILE = "/etc/luxbox/rgb.data"
FADETIME = 2
FADEFRAMERATE = 30
FADETOTALFRAMES = FADEFRAMERATE * FADETIME

print("Listening at ip: ", UDP_IP, ":", UDP_PORT)

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ws2811.init()

# Loading rgb setting
try:
  f = open(RGBFILE, 'r')
  rgbdata = f.read().split(',')
  try:
    r = int(rgbdata[0])
  except IndexError:
    r = 0
    
  try:
    g = int(rgbdata[1])
  except IndexError:
    g = 0

  try:
    b = int(rgbdata[2])
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
  #print("received message: ", data)
  jsondata = json.loads( str(data, "utf-8") );
  for area in jsondata['areas']:
    #print(area)
    for value in area['values']:
      #print(value)
      if value['color'] == 'r':
        targetRed = value['value']
      elif value['color'] == 'g':
        targetGreen = value['value']
      elif value['color'] == 'b':
        targetBlue = value['value']
      else:
        print("Received unknown color")

    stepRed = (targetRed - r) / FADETOTALFRAMES
    stepGreen = (targetGreen - g) / FADETOTALFRAMES
    stepBlue = (targetBlue - b) / FADETOTALFRAMES
    #print("Fading to "+str(targetRed)+","+str(targetGreen)+","+str(targetBlue))
    #print("Fading from "+str(r)+","+str(g)+","+str(b))
    #print("Steps to "+str(stepRed)+","+str(stepGreen)+","+str(stepBlue))
    for frame in range(0,FADETOTALFRAMES):
      newRed = int( r + (frame * stepRed))
      newGreen = int( g + (frame * stepGreen))
      newBlue = int( b + (frame * stepBlue))
      #print("New is "+str(newRed)+","+str(newGreen)+","+str(newBlue))
      ws2811.render( newRed, newGreen, newBlue )
      time.sleep(FADETIME / FADETOTALFRAMES)

    # Reached target color
    r = targetRed
    g = targetGreen
    b = targetBlue
    ws2811.render( r, g, b )
    
    try:
      f = open(RGBFILE, 'w')
      f.write( str(r) + ",")
      f.write( str(g) + ",")
      f.write( str(b))
      f.close() 
    except IOError:
      print("Failed to save rgb values!")

ws2811.fini()
	
  



