#!/usr/bin/python3

# vim: tabstop=2 shiftwidth=2 expandtab

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

red = 0
green = 0
blue = 0

def tryLoading():
  global RGBFILE

  global red
  global green
  global blue

  try:
    f = open(RGBFILE, 'r')
    rgbdata = f.read().split(',')
    try:
      red = int(rgbdata[0])
    except IndexError:
      red = 0
      
    try:
      green = int(rgbdata[1])
    except IndexError:
      green = 0
  
    try:
      blue = int(rgbdata[2])
    except IndexError:
      blue = 0
  
    print("Loaded from file: ")
    print("red:   " + str(red))
    print("green: " + str(green))
    print("blue:  " + str(blue))
    f.close()
  except IOError:
    print("Found no rgb.data. Expect luxbox server")

def save(r,g,b):
  global RGBFILE

  try:
    f = open(RGBFILE, 'w')
    f.write( str(r) + ",")
    f.write( str(g) + ",")
    f.write( str(b))
    f.close() 
  except IOError:
    print("Failed to save rgb values!")


def fadeTo( r, g, b):
  global red
  global green
  global blue

  global FADETOTALFRAMES
  global FADETIME

  stepRed = (r - red) / FADETOTALFRAMES
  stepGreen = (g - green) / FADETOTALFRAMES
  stepBlue = (b - blue) / FADETOTALFRAMES
  for frame in range(0,FADETOTALFRAMES):
    tempRed = int( red + (frame * stepRed))
    tempGreen = int( green + (frame * stepGreen))
    tempBlue = int( blue + (frame * stepBlue))
    ws2811.render( tempRed, tempGreen, tempBlue )
    time.sleep(FADETIME / FADETOTALFRAMES)
  
  # Reached target color
  red = r
  green = g
  blue = b
  ws2811.render( red, green, blue )


def main():
  global red
  global green
  global blue
 
  global UDP_IP
  global UDP_PORT

  print("Listening at ip: ", UDP_IP, ":", UDP_PORT)
  sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((UDP_IP, UDP_PORT))
  
  ws2811.init()
  
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

      fadeTo(targetRed, targetGreen, targetBlue )
      save( targetRed, targetGreen, targetBlue )
  
  ws2811.fini()
	

if __name__ == '__main__':
  main()
else:
  print("Run this script as __main__!")
  



