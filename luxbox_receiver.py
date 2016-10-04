import socket
import sys
import ws2811
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 11111

print("listening at ip: ", UDP_IP, ":", UDP_PORT)

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ws2811.init()

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

ws2811.fini()
	
  


