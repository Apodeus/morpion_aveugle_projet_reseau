#!/usr/bin/env python3
from socket import *
import select
import threading

from grid import *
import random
import sys

import re

ip=''
port = 7777

play_mode = 0;
expect_answer = 0;
class thread_r(threading.Thread):
	def __init__(self, s):
		threading.Thread.__init__(self)
		self.socket_client = s

	def run(self):
		while(True):
			data = bytes.decode(self.socket_client.recv(1024) )
			if (len(data) != 0):
				sen = re.findall('\$[a-zA-Z0-9]+', data)
				if sen:
					for i in range(len(sen)):
						w = sen[i]
						if w == "$gamestart":
							print("Début de la partie")
						elif data == "$play":
							print("Quelle case allez vous jouer ? (0-8)")
							play_mode = 1;
				else:
					print(data)

class thread_s(threading.Thread):
	def __init__(self, s):
		threading.Thread.__init__(self)
		self.socket_client = s

	def run(self):
		while True:
			text = input("")
			if play_mode == 1:
				self.socket_client.send(str.encode(str(int(text))))
			else:
				self.socket_client.send(str.encode(text))


def selectCase():

	choix = -1
	while(choix < 0 or choix > 8):
		choix = int(input("Quelle case allez vous jouer ? (0-8)"))

	return choix

def main():

	socket_client = socket(AF_INET6, SOCK_STREAM)
	socket_client.connect((ip, port))
	tr = thread_r(socket_client)
	ts = thread_s(socket_client)

	tr.start()
	ts.start()
	# while(True):
	# 	data = bytes.decode(socket_client.recv(1024) )
	# 	shot = -1
	# 	if data == "begin":
	# 		shot = selectCase()
	# 		socket_client.send( str.encode(str(shot) ))
	# 		data = None
	# 	else:
	# 		if(len(data) != 0):
	# 			print(data)
	#socket_client.close()

main()