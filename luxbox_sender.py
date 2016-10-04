import socket
import sys



UDP_IP = "192.168.10.255"
UDP_PORT = 11110
MESSAGE = """{
		"light_id": "hackermap",
		"name": "Hackermap",
		"areas": [
				{
						"number": 0,
						"name": "BackgroundLight",
						"color_type": "rgb",
						"supported_modes": "0",
						"values": [
								{
										"color": "r"
								},
								{
										"color": "g"
								},
								{
										"color": "b"
								}
						]
				}
		]

}"""

print("UDP target ip: ", UDP_IP)
print("UDP target port: ", UDP_PORT)


sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto( bytes( MESSAGE, "utf-8") , (UDP_IP, UDP_PORT))

